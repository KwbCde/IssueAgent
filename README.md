# 🧠 IssueAgent – Auto-Responding GitHub Issues with LLaMA3 & FastAPI

This project listens for new GitHub issues, analyzes them using LLaMA3 (via Ollama), and auto-comments back using the GitHub API.

---

## 🔧 Setup & Run (Dev Mode)

1. **Activate Virtual Environment**
```bash
cd IssueAgent-backend
.\venv\Scripts\activate
```

2. **Start Ollama and Load LLaMA3**
Open a second terminal and run:
```bash
ollama run llama3
```
> 🔄 Leave this terminal running — it's serving the local AI model.

3. **Run FastAPI App**
Back in your main terminal:
```bash
uvicorn main:app --reload
```
> 🌐 FastAPI will run at `http://127.0.0.1:8000`

4. **Expose FastAPI to the Internet (Ngrok)**
Open a third terminal:
```bash
ngrok http 8000
```
> Copy the HTTPS URL Ngrok gives you (e.g. `https://xyz.ngrok-free.app`)

5. **Connect GitHub Webhook**
- Go to your GitHub repo → Settings → Webhooks
- Click **Add webhook**
- Payload URL: `https://xyz.ngrok-free.app/webhook`
- Content type: `application/json`
- Select: Just the **Issues** event
- Save

Now, when you create an issue, it should trigger the webhook.

---

## ✅ What’s Done
- FastAPI webhook receiving GitHub issues
- LLaMA3 (via Ollama) analyzes issue title/body
- Webhook working through Ngrok
- Terminal prints LLaMA3 response ✅

---

## 🚧 Next Steps
- [ ] Build GitHub API response logic in `github_api.py`
- [ ] Automatically comment back on issues using GitHub API
  - Reference: https://docs.github.com/en/rest/issues/comments?apiVersion=2022-11-28#create-an-issue-comment

---

## 🔐 GitHub API Auth (Upcoming)
- Generate a **GitHub Personal Access Token**
- Scopes required: `repo`, `public_repo`
- You’ll need this token to authenticate POST requests to comment on issues

---

## 🌅 Tomorrow Startup Checklist
1. Open VS Code
2. `.\venv\Scripts\activate`
3. Terminal 1: `ollama run llama3`
4. Terminal 2: `uvicorn main:app --reload`
5. Terminal 3: `ngrok http 8000`
6. Test: Create a new GitHub issue — response will show in terminal

---

## 📁 Folder Structure
```
IssueAgent-backend/
├── main.py           # FastAPI app w/ webhook
├── llama_utils.py    # LLaMA3 prompt handler
├── github_api.py     # (to build) GitHub comment logic
├── venv/             # Python virtual environment
├── README.md         # Setup instructions
```

---

## 🧠 Built With
- FastAPI
- Ollama + LLaMA3
- Ngrok
- GitHub REST API

---

## 🎯 Goal
Automatically analyze and respond to GitHub issues with local AI, using FastAPI and GitHub webhooks.
