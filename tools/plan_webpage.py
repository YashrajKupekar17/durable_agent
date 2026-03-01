# tools/plan_webpage.py
import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

def plan_webpage(args: dict) -> dict:
    """Takes the spec and produces a detailed technical blueprint."""
    spec = args.get("spec")

    llm_model = os.environ.get("LLM_MODEL", "openai/gpt-4o")
    llm_key = os.environ.get("LLM_KEY")

    prompt = f"""You are a senior web architect.
Given this spec: {spec}

Produce a detailed technical plan in JSON:
{{
  "colorPalette": {{"primary": "", "secondary": "", "accent": "", "background": "", "text": ""}},
  "typography": {{"heading": "", "body": "", "sizes": {{}}}},
  "layout": "description of overall layout approach",
  "sections": [
    {{"name": "", "purpose": "", "elements": [], "notes": ""}}
  ],
  "cssApproach": "flexbox/grid/both",
  "animations": [],
  "jsFeatures": [],
  "accessibilityNotes": "",
  "vibe": "{spec.get('vibe', 'modern')}"
}}

Return ONLY valid JSON. No markdown fences, no explanation."""

    response = completion(
        model=llm_model,
        messages=[{"role": "user", "content": prompt}],
        api_key=llm_key,
    )

    plan_text = response.choices[0].message.content.strip()
    if plan_text.startswith("```"):
        plan_text = plan_text.split("\n", 1)[1]
        plan_text = plan_text.rsplit("```", 1)[0].strip()

    import json
    try:
        plan = json.loads(plan_text)
    except json.JSONDecodeError:
        plan = {"raw_plan": plan_text}

    return {"status": "planned", "plan": plan}
