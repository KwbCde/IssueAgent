from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1") 

def analyze_issue_with_llama(title: str, body: str) -> str:
    prompt = f"Github issue title: {title}\nIssue description: {body}\nWrite a helpful comment to respond to this issue."
    try:
        response = client.chat.completions.create(
            model="llama3:latest",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        result = response.choices[0].message.content
        return result
    except Exception as e:
        return f"Error calling local LLaMa: {e}"