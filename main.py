import os
import hmac
import hashlib
import jwt
import time
import httpx
from fastapi import FastAPI, Request, Header, HTTPException
from app.llm_utils import analyze_issue_with_llm

app = FastAPI()
conversation_history = {}

GITHUB_APP_ID = os.getenv("GITHUB_APP_ID")
PRIVATE_KEY = os.getenv("GITHUB_PRIVATE_KEY").replace("\\n", "\n")
WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")

def verify_signature(payload_body: bytes, signature_header: str):
    sha_name, signature = signature_header.split("=")
    if sha_name != "sha256":
        raise ValueError("Unsupported signature algorithm")
    mac = hmac.new(WEBHOOK_SECRET.encode(), msg=payload_body, digestmod=hashlib.sha256)
    if not hmac.compare_digest(mac.hexdigest(), signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

def generate_jwt():
    now = int(time.time())
    payload = {
        "iat": now,
        "exp": now + 540,
        "iss": GITHUB_APP_ID
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")

def get_installation_token(installation_id):
    token = generate_jwt()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    response = httpx.post(url, headers=headers)
    response.raise_for_status()
    return response.json()["token"]

def comment_on_issue(owner, repo, issue_number, comment, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    httpx.post(url, headers=headers, json={"body": comment})

@app.post("/webhook")
async def github_webhook(request: Request, x_hub_signature_256: str = Header(None)):
    raw_body = await request.body()
    if WEBHOOK_SECRET:
        verify_signature(raw_body, x_hub_signature_256)

    payload = await request.json()
    event = request.headers.get("X-GitHub-Event")

    if event not in ["issues", "issue_comment"]:
        return {"status": "ignored"}

    action = payload.get("action")
    if event == "issues" and action == "opened":
        issue = payload["issue"]
        repo = payload["repository"]
        title = issue["title"]
        body = issue["body"]
        issue_number = issue["number"]
        owner = repo["owner"]["login"]
        repo_name = repo["name"]
        installation_id = payload["installation"]["id"]

        key = f"{owner}/{repo_name}#{issue_number}"
        if key not in conversation_history:
            conversation_history[key] = [
                {"role": "system", "content": "You are a helpful GitHub assistant."}
            ]
        conversation_history[key].append({
            "role": "user",
            "content": f"Github issue title: {title}\nIssue description: {body}\nWrite a helpful comment to respond to this issue."
        })

        llm_response = analyze_issue_with_llm(conversation_history[key])
        conversation_history[key].append({"role": "assistant", "content": llm_response})

        token = get_installation_token(installation_id)
        comment_on_issue(owner, repo_name, issue_number, llm_response, token)
        return {"status": "ok"}

    elif event == "issue_comment" and action == "created":
        comment = payload["comment"]
        commenter = comment["user"]["type"]
        if commenter == "Bot":
            return {"status": "ignored", "reason": "Bot comment"}

        issue = payload["issue"]
        repo = payload["repository"]
        title = issue["title"]
        body = issue["body"]
        issue_number = issue["number"]
        owner = repo["owner"]["login"]
        repo_name = repo["name"]
        installation_id = payload["installation"]["id"]

        key = f"{owner}/{repo_name}#{issue_number}"
        if key not in conversation_history:
            conversation_history[key] = [
                {"role": "system", "content": "You are a helpful GitHub assistant."},
                {"role": "user", "content": f"Github issue title: {title}\nIssue description: {body}\nWrite a helpful comment to respond to this issue."}
            ]
        conversation_history[key].append({"role": "user", "content": comment["body"]})
        llm_response = analyze_issue_with_llm(conversation_history[key])
        conversation_history[key].append({"role": "assistant", "content": llm_response})

        token = get_installation_token(installation_id)
        comment_on_issue(owner, repo_name, issue_number, llm_response, token)
        return {"status": "ok"}

    return {"status": "ignored"}
