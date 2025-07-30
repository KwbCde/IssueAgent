
---

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)

## IssueAgent

**IssueAgent** is a GitHub App backend built with FastAPI that listens for issue events then analyzes them using an LLM (via OpenAI) and posts context relevant comments back on GitHub issues. It’s designed for full automation and secure deployment using best practices.

---


## Try It Out
The IssueAgent GitHub App is live and available for installation:

[Install IssueAgent on Your Repo](https://github.com/apps/issueagent)

Once installed it will automatically reply to new issues and comments using an LLM.

---


## Features

* Responds automatically to new GitHub issues and comments
* Analyzes issue content using OpenAI’s GPT model
* Posts helpful, relevant replies directly to the issue thread
* Stores lightweight conversation context to maintain thread relevance
* Securely validates webhook signatures
* Authenticates using GitHub App JWT and installation tokens
* Deployable on platforms like Railway with no extra configuration

---

## Why Use IssueAgent?

Managing GitHub issues can be time consuming especially for busy maintainers and teams. IssueAgent automates issue triaging and responses using AI helping you:

- Save time by automatically providing relevant suggestions and guidance
- Improve issue response quality and consistency
- Maintain context-aware conversations without manual follow-up
- Securely integrate with your workflow without additional infrastructure
- Deploy easily on popular cloud platforms with minimal setup

By automating routine interactions, IssueAgent lets you focus on coding and important tasks instead of repetitive issue management.

---

## Tech Stack

* **Backend**: FastAPI
* **AI Integration**: OpenAI SDK (gpt-3.5-turbo)
* **Authentication**: JWT + GitHub App installation tokens
* **Deployment**: Railway (Dockerless)
* **HTTP Clients**: httpx, requests
* **Environment Config**: python-dotenv

---

## Getting Started

### Prerequisites

* Python 3.11+
* GitHub account and GitHub App created
* OpenAI API key (or compatible API provider)
* Railway (or any cloud platform) for deployment

### Installation

1. Clone the repo:

   
```bash
   git clone https://github.com/KwbCde/IssueAgent.git
   cd IssueAgent
   ```
   

2. Create a virtual environment:

   
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   
```bash
   pip install -r requirements.txt
```


4. Create a .env file in the project root:

   
```dotenv
   GITHUB_APP_ID=your_github_app_id
   GITHUB_PRIVATE_KEY=your_github_private_key
   GITHUB_WEBHOOK_SECRET=your_webhook_secret
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_BASE_URL=https://api.openai.com/v1  # Optional if using default
```


---

## Running Locally

Start the server:

```bash
uvicorn main:app --reload
```


The server will run at http://localhost:8000.

To test GitHub webhook events locally consider using [ngrok](https://ngrok.com/):

```bash
ngrok http 8000
```


---

## Deployment

IssueAgent is optimized for deployment on [Railway](https://railway.app):

1. Push to a public GitHub repo
2. Deploy directly via Railway GitHub integration
3. Set your environment variables securely in the Railway dashboard

Your /webhook endpoint will then be available for GitHub to call.

---

## GitHub App Setup

1. Create a [GitHub App](https://github.com/settings/apps)
2. Enable webhook events: issues and issue_comment
3. Set the webhook URL to: https://your-app-url/webhook
4. Grant the app **Read & Write** permissions for **Issues**
5. Generate and upload your private key to the .env

After installation on a repository, the app will automatically respond to new issues and comments.

---

## Project Structure

```text
IssueAgent/
│
├── app/
│   ├── __init__.py
│   ├── llm_utils.py        # OpenAI interaction logic
│   └── github_api.py       # GitHub REST API functions
│
├── main.py                 # Webhook server and routing
├── requirements.txt
├── .env                    # Environment variables (not committed)
└── README.md
```

---

## Learning Goals

I created **IssueAgent** to deepen my understanding of backend APIs, GitHub automation, and AI-assisted development tools. Through this project I gained practical experience with:

* Structuring a FastAPI application for production use
* Secure webhook verification and GitHub App authentication (JWT + installation tokens)
* Building reliable GitHub bots that interact via REST API
* Contextual prompt engineering and LLM output handling
* Deployment on cloud platforms using environment-based configuration
* Writing clean, modular code for real-world automation workflows

---

## Contributing

Contributions are welcome. If you'd like to help improve IssueAgent please:

- Open an issue to discuss your idea or report bugs
- Fork the repository and create a feature branch for your changes
- Follow the existing code style and add tests when applicable
- Submit a pull request with a clear description of your changes

---

## Future Work

Planned improvements include:

- Enhanced context tracking for longer issue conversations
- Support for additional GitHub events, like pull requests and reviews
- Customizable AI response templates based on repository settings
- Improved error handling and logging for production environments
- Integration with other AI providers and models

---

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---
