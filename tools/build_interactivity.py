# tools/build_interactivity.py
import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

def build_interactivity(args: dict) -> dict:
    """Generates vanilla JS for interactive features."""
    html = args.get("html")
    plan = args.get("plan")

    js_features = []
    if isinstance(plan, dict):
        js_features = plan.get("jsFeatures", [])

    if not js_features:
        return {"status": "no_js_needed", "js": ""}

    llm_model = os.environ.get("LLM_MODEL", "openai/gpt-4o")
    llm_key = os.environ.get("LLM_KEY")

    prompt = f"""You are a JavaScript specialist.
Given this HTML: {html}
Implement these features: {js_features}

Rules:
- Vanilla JS only, no external libraries
- Wrap everything in DOMContentLoaded
- Handle edge cases gracefully
- Accessible (keyboard navigable where applicable)
- Use querySelector with the exact class/id names from the HTML

Return ONLY the raw JavaScript code. No markdown, no explanation."""

    response = completion(
        model=llm_model,
        messages=[{"role": "user", "content": prompt}],
        api_key=llm_key,
    )

    js = response.choices[0].message.content.strip()
    if js.startswith("```"):
        js = js.split("\n", 1)[1]
        js = js.rsplit("```", 1)[0].strip()

    return {"status": "interactivity_built", "js": js}
