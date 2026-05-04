import html
import json
from pathlib import Path

from app import app


def build_redoc_html(spec: dict, page_title: str = "Flask User API Documentation") -> str:
    spec_json = json.dumps(spec, ensure_ascii=True)
    safe_title = html.escape(page_title, quote=True)
    return f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{safe_title}</title>
    <style>
      body {{
        margin: 0;
        padding: 0;
      }}
    </style>
  </head>
  <body>
    <div id="redoc-container"></div>
    <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
    <script>
      const spec = {spec_json};
      Redoc.init(spec, {{}}, document.getElementById("redoc-container"));
    </script>
  </body>
</html>
"""


def main() -> None:
    output_file = Path("docs") / "redoc-static.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with app.test_client() as client:
        response = client.get("/openapi.json")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to get OpenAPI spec. Status code: {response.status_code}"
            )
        spec = response.get_json()
        if not spec:
            raise RuntimeError("OpenAPI spec is empty or invalid JSON.")

    output_file.write_text(build_redoc_html(spec), encoding="utf-8")
    print(f"Generated static ReDoc HTML at: {output_file.resolve()}")


if __name__ == "__main__":
    main()
