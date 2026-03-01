# tools/build_styles.py
import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

def build_styles(args: dict) -> dict:
    """Generates complete CSS from the HTML structure and plan."""
    html = args.get("html")
    plan = args.get("plan")

    llm_model = os.environ.get("LLM_MODEL", "openai/gpt-4o")
    llm_key = os.environ.get("LLM_KEY")

    vibe = "modern"
    if isinstance(plan, dict):
        vibe = plan.get("vibe", "modern")

    prompt = f"""You are a CSS specialist.
Given this HTML: {html}
And this design plan: {plan}

Write complete CSS. Rules:
- CSS custom properties (variables) for all colors and fonts at :root
- Mobile-first, fully responsive with media queries
- Smooth transitions on interactive elements (buttons, links, cards)
- Match the vibe: {vibe}
- Use the exact class names from the HTML
- Beautiful spacing, typography, and visual hierarchy
- NO javascript

Return ONLY the raw CSS code. No markdown, no explanation, no selectors wrapping."""

    response = completion(
        model=llm_model,
        messages=[{"role": "user", "content": prompt}],
        api_key=llm_key,
    )

    css = response.choices[0].message.content.strip()
    if css.startswith("```"):
        css = css.split("\n", 1)[1]
        css = css.rsplit("```", 1)[0].strip()

    return {"status": "styles_built", "css": css}
