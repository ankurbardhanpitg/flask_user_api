# API Documentation Guide

This project supports API docs in 3 formats:

- Live ReDoc/Swagger from the running Flask app
- Static ReDoc HTML file
- Static PDF file

## Setup

```bash
pip install -r requirements.txt
```

## Run API Server

```bash
python app.py
```

Then open:

- ReDoc: `http://127.0.0.1:5000/redoc`
- Swagger: `http://127.0.0.1:5000/swagger`
- OpenAPI JSON: `http://127.0.0.1:5000/openapi.json`

## Generate Static ReDoc HTML

```bash
python generate_redoc_static.py
```

Output:

- `docs/redoc-static.html`

## Generate PDF API Docs

```bash
python generate_pdf_static.py
```

Output:

- `docs/api-docs.pdf`
- If the file is open/locked, a timestamped PDF is created in `docs/`.

## Notes

- `openapi_spec.py` is the source of truth for all docs.
- Update the spec first, then regenerate HTML/PDF.
- Protected APIs show Bearer token requirement in generated docs.
