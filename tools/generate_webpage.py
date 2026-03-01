import os
import json
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

def generate_webpage(args: dict) -> dict:
    """Uses LLM to generate a single-file HTML/CSS/JS webpage."""
    description = args.get("description")
    style_preferences = args.get("stylePreferences", "modern, clean")
    
    llm_model = os.environ.get("LLM_MODEL", "openai/gpt-4o")
    llm_key = os.environ.get("LLM_KEY")

    prompt = f"""Create a complete, beautiful single-file HTML page based on this description:

Description: {description}
Style preferences: {style_preferences}

Requirements:
- Everything in ONE .html file (inline CSS in <style> tag, inline JS in <script> tag)
- Modern, responsive design
- Use a pleasing color palette
- Clean typography
- No external dependencies except Google Fonts if needed
- Must be fully functional and visually impressive

Return ONLY the raw HTML code, nothing else. No markdown, no explanation."""

    response = completion(
        model=llm_model,
        messages=[{"role": "user", "content": prompt}],
        api_key=llm_key,
    )

    html_content = response.choices[0].message.content.strip()
    
    # Strip markdown code fences if present
    if html_content.startswith("```"):
        html_content = html_content.split("\n", 1)[1]
        html_content = html_content.rsplit("```", 1)[0].strip()

    return {
        "status": "generated",
        "html_content": html_content,
        "description": description,
    }