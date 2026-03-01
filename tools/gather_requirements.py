# tools/gather_requirements.py

def gather_requirements(args: dict) -> dict:
    """Structures user answers into a clean spec dict. No LLM call needed."""
    return {
        "status": "requirements_gathered",
        "spec": {
            "purpose": args.get("purpose"),
            "audience": args.get("audience"),
            "vibe": args.get("vibe"),
            "sections": args.get("sections"),
            "interactivity": args.get("interactivity"),
            "colorPreferences": args.get("colorPreferences"),
            "content": args.get("content"),
        }
    }
