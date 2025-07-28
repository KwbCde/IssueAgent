from fastapi import FastAPI, Request
from app.llm_utils import analyze_issue_with_llama
from app.github_api import comment_on_issue

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "API is running"}

@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()
    action = payload.get("action")

    if action != "opened":
        return {"status": "ignored", "reason": "Not a new issue"}
    issue = payload.get("issue" or {})
    repo = payload.get("repository" or {})
    title = issue.get("title")
    body = issue.get("body")
    issue_number = issue.get("number")
    owner = repo.get("owner", {}).get("login")
    repo_name = repo.get("name")

    llm_response = analyze_issue_with_llama(title, body)

    comment_on_issue(owner, repo_name, issue_number, llm_response)

    print("LLM Response:\n", llm_response)


    return {
        "status": "ok",
        "action": action,
        "title": title,
        "llm_response": llm_response
    }