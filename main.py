from fastapi import FastAPI, Request
from app.llm_utils import analyze_issue_with_llm
from app.github_api import comment_on_issue

app = FastAPI()

conversation_history = {}

@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()
    action = payload.get("action")

    if action != "opened":
        return {"status": "ignored", "reason": "Not a new issue"}

    issue = payload.get("issue") or {}
    repo = payload.get("repository") or {}
    title = issue.get("title")
    body = issue.get("body")
    issue_number = issue.get("number")
    owner = repo.get("owner", {}).get("login")
    repo_name = repo.get("name")

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

    conversation_history[key].append({
        "role": "assistant",
        "content": llm_response
    })

    comment_on_issue(owner, repo_name, issue_number, llm_response)

    return {
        "status": "ok",
        "action": action,
        "title": title,
        "llm_response": llm_response
    }
