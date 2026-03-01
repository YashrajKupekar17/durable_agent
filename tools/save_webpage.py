import os

def save_webpage(args: dict) -> dict:
    """Saves the generated HTML to a file and returns the file path."""
    html_content = args.get("htmlContent")
    filename = args.get("filename", "output.html")

    # Sanitize filename
    if not filename.endswith(".html"):
        filename += ".html"
    filename = filename.replace(" ", "_").lower()

    output_dir = os.path.join(os.getcwd(), "generated_pages")
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

    return {
        "status": "saved",
        "filename": filename,
        "filepath": filepath,
        "previewUrl": f"http://localhost:8000/preview/{filename}",
    }