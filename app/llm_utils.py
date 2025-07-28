import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL") or None

client = OpenAI(base_url=base_url or None, api_key=api_key) 

def analyze_issue_with_llm(conversation_history) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_history,
            temperature=0.7,
            max_tokens =500,
            n=1,
            stop=None,
        )
        result = response.choices[0].message.content
        return result
    except Exception as e:
        return f"Error calling OpenAI API: {e}"
