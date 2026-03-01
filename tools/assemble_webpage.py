# tools/assemble_webpage.py

def assemble_webpage(args: dict) -> dict:
    """Combines HTML + CSS + JS into a single file. No LLM needed."""
    html = args.get("html")
    css = args.get("css")
    js = args.get("js", "")

    # Inject CSS before </head>
    if "</head>" in html:
        assembled = html.replace(
            "</head>",
            f"<style>\n{css}\n</style>\n</head>"
        )
    else:
        assembled = f"<style>\n{css}\n</style>\n{html}"

    # Inject JS before </body> if there is any
    if js:
        if "</body>" in assembled:
            assembled = assembled.replace(
                "</body>",
                f"<script>\n{js}\n</script>\n</body>"
            )
        else:
            assembled += f"\n<script>\n{js}\n</script>"

    return {
        "status": "assembled",
        "html_content": assembled,
    }
