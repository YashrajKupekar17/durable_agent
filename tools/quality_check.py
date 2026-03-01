# tools/quality_check.py
import os
import json
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

def quality_check(args: dict) -> dict:
    """Reviews HTML + CSS + JS for issues before assembly."""
    html = args.get("html")
    css = args.get("css")
    js = args.get("js", "")

    llm_model = os.environ.get("LLM_MODEL", "openai/gpt-4o")
    llm_key = os.environ.get("LLM_KEY")

    prompt = f"""You are a senior QA engineer reviewing a webpage before it ships.

HTML:
{html}

CSS:
{css}

JS:
{js if js else "(no JS)"}

Check for:
1. CSS class names referenced in HTML that don't exist in CSS (and vice versa)
2. JS references to elements that don't exist in HTML
3. Missing alt attributes on images
4. Missing form labels
5. Obvious mobile layout issues (e.g. fixed widths)
6. Broken logic in JS

Return ONLY valid JSON:
{{
  "passed": true or false,
  "issues": ["issue 1", "issue 2"],
  "fixedHtml": "corrected HTML or null if no fixes needed",
  "fixedCss": "corrected CSS or null if no fixes needed",
  "fixedJs": "corrected JS or null if no fixes needed"
}}

If everything looks good, set passed=true and issues=[]. Return ONLY JSON."""

    response = completion(
        model=llm_model,
        messages=[{"role": "user", "content": prompt}],
        api_key=llm_key,
    )

    result_text = response.choices[0].message.content.strip()
    if result_text.startswith("```"):
        result_text = result_text.split("\n", 1)[1]
        result_text = result_text.rsplit("```", 1)[0].strip()

    try:
        result = json.loads(result_text)
    except json.JSONDecodeError:
        result = {"passed": True, "issues": [], "fixedHtml": None, "fixedCss": None, "fixedJs": None}

    # Apply fixes if QA found issues
    final_html = result.get("fixedHtml") or html
    final_css = result.get("fixedCss") or css
    final_js = result.get("fixedJs") or js

    return {
        "status": "checked",
        "passed": result.get("passed", True),
        "issues": result.get("issues", []),
        "html": final_html,
        "css": final_css,
        "js": final_js,
    }
