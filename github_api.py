import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

def comment_on_issue(owner, repo, issue_number, comment_text):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    
    data = {
        "body": comment_text
    }
    
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("Comment created successfully")
        print(response.json())
    else:
        print("Failed to create comment")
        print("Status Code:", response.status_code)
        print("Response:", response.text)

