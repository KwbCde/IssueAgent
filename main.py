from fastapi import FastAPI, Request
from llama_utils import analyze_issue_with_llama

app = FastAPI()

@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()
    action = payload.get("action")
    issue = payload.get("issue", {})
    title = issue.get("title")
    body = issue.get("body")

    llama_response = analyze_issue_with_llama(title, body)

    print("LLaMA Response:\n", llama_response)


    return {
        "status": "ok",
        "action": action,
        "title": title,
        "llama_response": llama_response
    }

