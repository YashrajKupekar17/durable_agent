# tools/explain_webpage.py
import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

def explain_webpage(args: dict) -> dict:
    html_content = args.get("htmlContent")
    question = args.get("question")  # e.g. "what CSS did you use for the layout?"

    llm_model = os.environ.get("LLM_MODEL", "openai/gpt-4o")
    llm_key = os.environ.get("LLM_KEY")

    prompt = f"""A user is looking at this webpage and has a question about it.
Answer clearly and simply — they may not be a developer.

HTML:
{html_content}

Question: {question}

Give a short, friendly explanation."""

    response = completion(
        model=llm_model,
        messages=[{"role": "user", "content": prompt}],
        api_key=llm_key,
    )

    return {
        "status": "explained",
        "explanation": response.choices[0].message.content.strip(),
    }