"""Generate static ReDoc HTML from `pam_project_spec.PAM_PROJECT_SPEC`."""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from generate_redoc_static import build_redoc_html

from pam_project.pam_project_spec import PAM_PROJECT_SPEC


def main() -> None:
    output_file = _ROOT / "docs" / "pam-redoc-static.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    page_title = PAM_PROJECT_SPEC.get("info", {}).get("title", "PAM API Documentation")

    output_file.write_text(
        build_redoc_html(PAM_PROJECT_SPEC, page_title=page_title),
        encoding="utf-8",
    )
    print(f"Generated static PAM ReDoc HTML at: {output_file.resolve()}")


if __name__ == "__main__":
    main()
