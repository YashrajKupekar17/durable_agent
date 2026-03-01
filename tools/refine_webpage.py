# tools/refine_webpage.py
import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

def refine_webpage(args: dict) -> dict:
    current_html = args.get("currentHtml")
    refinement = args.get("refinement")  # e.g. "make buttons bigger, change bg to dark"

    llm_model = os.environ.get("LLM_MODEL", "openai/gpt-4o")
    llm_key = os.environ.get("LLM_KEY")

    prompt = f"""You are editing an existing HTML webpage. 
Apply ONLY the requested changes, keep everything else identical.

Current HTML:
{current_html}

Requested changes:
{refinement}

Return ONLY the complete updated HTML file. No explanation, no markdown."""

    response = completion(
        model=llm_model,
        messages=[{"role": "user", "content": prompt}],
        api_key=llm_key,
    )

    updated_html = response.choices[0].message.content.strip()
    if updated_html.startswith("```"):
        updated_html = updated_html.split("\n", 1)[1]
        updated_html = updated_html.rsplit("```", 1)[0].strip()

    return {
        "status": "refined",
        "html_content": updated_html,
        "refinement_applied": refinement,
    }