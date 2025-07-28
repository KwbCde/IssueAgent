from fastapi import FastAPI, Request
from app.llm_utils import analyze_issue_with_llm
from app.github_api import comment_on_issue

app = FastAPI()

conversation_history = {}

@app.post("/webhook")
async def github_webhook(request: Request):
    event = request.headers.get("X-GitHub-Event")
    payload = await request.json()

    if event == "issues" and payload.get("action") == "opened":
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

        return {"status": "ok"}

    elif event == "issue_comment" and payload.get("action") == "created":
        comment = payload.get("comment") or {}
        issue = payload.get("issue") or {}
        repo = payload.get("repository") or {}
        comment_body = comment.get("body")
        issue_number = issue.get("number")
        owner = repo.get("owner", {}).get("login")
        repo_name = repo.get("name")
        title = issue.get("title")
        body = issue.get("body")

        key = f"{owner}/{repo_name}#{issue_number}"

        if key not in conversation_history:
            conversation_history[key] = [
                {"role": "system", "content": "You are a helpful GitHub assistant."},
                {"role": "user", "content": f"Github issue title: {title}\nIssue description: {body}\nWrite a helpful comment to respond to this issue."}
            ]

        conversation_history[key].append({
            "role": "user",
            "content": comment_body
        })

        llm_response = analyze_issue_with_llm(conversation_history[key])

        conversation_history[key].append({
            "role": "assistant",
            "content": llm_response
        })

        comment_on_issue(owner, repo_name, issue_number, llm_response)

        return {"status": "ok"}

    else:
        return {"status": "ignored", "reason": "Event/action not handled"}
