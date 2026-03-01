# tools/build_structure.py
import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

def build_structure(args: dict) -> dict:
    """Generates semantic HTML skeleton from the plan. No styles, no JS."""
    plan = args.get("plan")
    spec = args.get("spec")

    llm_model = os.environ.get("LLM_MODEL", "openai/gpt-4o")
    llm_key = os.environ.get("LLM_KEY")

    prompt = f"""You are an HTML specialist.
Using this plan: {plan}
And this spec: {spec}

Write ONLY the HTML structure. Rules:
- Full HTML5 document (<!DOCTYPE html>, <html>, <head>, <body>)
- Semantic tags (header, main, section, footer, nav)
- Meaningful class names that you will style later
- Placeholder content where real content isn't provided
- Include Google Fonts link in <head> if the plan specifies fonts
- NO inline styles, NO <style> tags
- NO javascript, NO <script> tags

Return ONLY the raw HTML code. No markdown, no explanation."""

    response = completion(
        model=llm_model,
        messages=[{"role": "user", "content": prompt}],
        api_key=llm_key,
    )

    html = response.choices[0].message.content.strip()
    if html.startswith("```"):
        html = html.split("\n", 1)[1]
        html = html.rsplit("```", 1)[0].strip()

    return {"status": "structure_built", "html": html}
