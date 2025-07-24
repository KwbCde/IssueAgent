---

# IssueAgent

IssueAgent is a backend service built with FastAPI that automates GitHub issue management. It listens for new GitHub issues, uses AI to analyze the issue content, and posts helpful, context-aware comments back to the issue thread.

---

## Features

* Receives webhook events from GitHub for new issues
* Uses a large language model (LLM) via OpenAI SDK to generate relevant issue responses
* Automatically posts AI-generated comments on GitHub issues
* Designed for easy deployment on platforms like Railway

---

## Tech Stack

* Python 3.11
* FastAPI
* OpenAI API (compatible with various LLM providers)
* GitHub REST API
* Requests
* dotenv for environment variable management

---

## Getting Started

### Prerequisites

* Python 3.11 or later
* GitHub account and a personal access token with repo permissions
* OpenAI API key or equivalent LLM API credentials

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/KwbCde/IssueAgent.git
   cd IssueAgent
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your environment variables:

   ```
   GITHUB_TOKEN=your_github_token_here
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_BASE_URL=your_openai_base_url_here  # optional depending on provider
   ```

### Running Locally

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

---

## Deployment

IssueAgent is set up to be deployed on cloud platforms such as Railway. Update your environment variables on your deployment platform with the appropriate keys.

---

## Usage

1. Configure your GitHub repository webhook to send issue events (specifically "issues" events) to your deployed `/webhook` endpoint.

2. When a new issue is opened, the webhook will trigger the backend to analyze the issue and post an AI-generated comment automatically.

---

## Project Structure

* `main.py` — FastAPI app handling webhook endpoints
* `app/__init__.py` - # Initializes the `app` package 
* `app/llm_utils.py` — AI integration logic for generating responses
* `app/github_api.py` — GitHub API wrapper to post comments
* `.env` — Environment variables (not included in repo)

---

## Notes

* The project currently supports integration with OpenAI-compatible LLM APIs but can be extended to other providers.
* The AI model and API base URL can be configured via environment variables.

---

## Architecture Diagram / API Flow

-- 
## Learning Goals

I created IssueAgent to deepen my understanding of backend API's webhooks, and deploying real-world AI applications. It helped me get experience with:

- FastAPI backend development and webhook handling
- Integration with OpenAI-compatible LLM API's
- GitHub webhooks and automation
- Secure environment variable management
- Deployment on cloud platforms

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---
