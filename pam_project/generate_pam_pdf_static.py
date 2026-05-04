"""Generate static API documentation PDF from `pam_project_spec.PAM_PROJECT_SPEC`."""

import sys
from pathlib import Path

# Repo root on sys.path so `generate_pdf_static` and `pam_project` resolve when run as a script.
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from generate_pdf_static import build_openapi_pdf_story, write_openapi_pdf

from pam_project.pam_project_spec import PAM_PROJECT_SPEC


def main() -> None:
    output_dir = _ROOT / "docs"
    output_file = output_dir / "pam-api-docs.pdf"
    story = build_openapi_pdf_story(PAM_PROJECT_SPEC)
    written = write_openapi_pdf(story, output_file)
    print(f"Generated PAM static PDF at: {written.resolve()}")


if __name__ == "__main__":
    main()
