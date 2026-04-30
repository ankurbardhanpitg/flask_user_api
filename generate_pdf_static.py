import json
from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import HRFlowable, Paragraph, Preformatted, SimpleDocTemplate, Spacer

from app import app


def _resolve_schema(schema: dict, components: dict, seen_refs: set[str] | None = None) -> dict:
    if not schema:
        return {}

    if seen_refs is None:
        seen_refs = set()

    ref = schema.get("$ref")
    prefix = "#/components/schemas/"

    if ref:
        if ref in seen_refs:
            return {}
        if not ref.startswith(prefix):
            return schema

        seen_refs.add(ref)
        schema_name = ref[len(prefix) :]
        resolved_ref_schema = components.get("schemas", {}).get(schema_name, {})
        return _resolve_schema(resolved_ref_schema, components, seen_refs)

    resolved = dict(schema)
    schema_type = resolved.get("type")
    if schema_type == "object":
        properties = resolved.get("properties", {})
        resolved["properties"] = {
            prop_name: _resolve_schema(prop_schema, components, set(seen_refs))
            for prop_name, prop_schema in properties.items()
        }
    elif schema_type == "array":
        resolved["items"] = _resolve_schema(
            resolved.get("items", {}), components, set(seen_refs)
        )

    return resolved


def _schema_lines(schema: dict, indent: int = 0) -> list[str]:
    if not schema:
        return []

    lines = []
    schema_type = schema.get("type", "object")
    prefix = "  " * indent
    lines.append(f"{prefix}- type: {schema_type}")

    if schema_type == "object":
        properties = schema.get("properties", {})
        required_fields = set(schema.get("required", []))
        for prop_name, prop_schema in properties.items():
            prop_type = prop_schema.get("type", "object")
            required = "required" if prop_name in required_fields else "optional"
            lines.append(f"{prefix}- {prop_name}: {prop_type} ({required})")
            if prop_type in {"object", "array"}:
                lines.extend(_schema_lines(prop_schema, indent + 1))
    elif schema_type == "array":
        items = schema.get("items", {})
        item_type = items.get("type", "object")
        lines.append(f"{prefix}- items: {item_type}")
        if item_type in {"object", "array"}:
            lines.extend(_schema_lines(items, indent + 1))

    return lines


def _format_parameter(param: dict) -> str:
    name = param.get("name", "unknown")
    where = param.get("in", "unknown")
    required = param.get("required", False)
    param_type = param.get("schema", {}).get("type", "object")
    return f"- {name} ({where}, type={param_type}, required={required})"


def _safe_para(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _security_lines(
    operation_security: list[dict] | None,
    global_security: list[dict] | None,
    components: dict,
) -> list[str]:
    security_requirements = (
        operation_security if operation_security is not None else (global_security or [])
    )
    if not security_requirements:
        return []

    schemes = components.get("securitySchemes", {})
    lines = []
    for requirement in security_requirements:
        if not isinstance(requirement, dict):
            continue
        for scheme_name, scopes in requirement.items():
            scheme_meta = schemes.get(scheme_name, {})
            scheme_type = scheme_meta.get("type", "unknown")
            scheme = scheme_meta.get("scheme")
            bearer_format = scheme_meta.get("bearerFormat")

            line = f"- {scheme_name}: type={scheme_type}"
            if scheme:
                line += f", scheme={scheme}"
            if bearer_format:
                line += f", bearerFormat={bearer_format}"
            if scopes:
                line += f", scopes={scopes}"
            lines.append(line)

    return lines


def _build_example_from_schema(schema: dict) -> object | None:
    if not schema:
        return None

    if "example" in schema:
        return schema["example"]

    schema_type = schema.get("type")
    if schema_type == "object":
        properties = schema.get("properties", {})
        if not properties:
            return None
        example_obj = {}
        for prop_name, prop_schema in properties.items():
            prop_example = _build_example_from_schema(prop_schema)
            if prop_example is not None:
                example_obj[prop_name] = prop_example
        return example_obj or None

    if schema_type == "array":
        item_example = _build_example_from_schema(schema.get("items", {}))
        if item_example is not None:
            return [item_example]
    return None


def _extract_example(media_meta: dict, schema: dict) -> object | None:
    if not media_meta:
        return None
    if "example" in media_meta:
        return media_meta["example"]
    examples = media_meta.get("examples", {})
    if isinstance(examples, dict):
        for example_meta in examples.values():
            if isinstance(example_meta, dict) and "value" in example_meta:
                return example_meta["value"]
    return _build_example_from_schema(schema)


def _example_text(example_value: object) -> str:
    if example_value is None:
        return ""
    return json.dumps(example_value, indent=4, ensure_ascii=True)


def main() -> None:
    with app.test_client() as client:
        response = client.get("/openapi.json")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to get OpenAPI spec. Status code: {response.status_code}"
            )
        spec = response.get_json()
        if not spec:
            raise RuntimeError("OpenAPI spec is empty or invalid JSON.")

    output_dir = Path("docs")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "api-docs.pdf"

    styles = getSampleStyleSheet()
    styles["Heading1"].textColor = colors.red
    styles["Heading2"].textColor = colors.blue
    styles["Heading3"].textColor = colors.green
    body_style = styles["BodyText"]
    bullet_style = ParagraphStyle(
        "DocBullet",
        parent=body_style,
        leftIndent=18,
        spaceAfter=3,
    )
    example_style = ParagraphStyle(
        "ExampleBlock",
        parent=bullet_style,
        backColor=colors.lightyellow,
        leftIndent=24,
        spaceBefore=2,
        spaceAfter=2,
        fontName="Courier",
    )
    example_label_style = ParagraphStyle(
        "ExampleLabel",
        parent=bullet_style,
        fontName="Helvetica-Bold",
        spaceBefore=8,
        spaceAfter=2,
    )

    story = []
    info = spec.get("info", {})
    components = spec.get("components", {})
    paths = spec.get("paths", {})
    global_security = spec.get("security")

    story.append(Paragraph(_safe_para(info.get("title", "API Documentation")), styles["Title"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"Version: {_safe_para(info.get('version', 'N/A'))}", body_style))
    if info.get("description"):
        story.append(Paragraph(_safe_para(info["description"]), body_style))
    story.append(Spacer(1, 14))

    for path, operations in paths.items():
        
        for method, details in operations.items():
            story.append(HRFlowable(width="100%", thickness=3, color=colors.grey))
            story.append(Spacer(1, 6))
            
            if details.get("summary"):
                story.append(
                    Paragraph(f"Api Name: {_safe_para(details['summary'])}", styles["Heading1"])
                )
            story.append(
                Paragraph(f"Api Path: {_safe_para(path)}", styles["Heading2"])
            )
            story.append(
                Paragraph(f"Api Method: {_safe_para(method.upper())}", styles["Heading3"])
            )
            if details.get("description"):
                story.append(Paragraph("Description:", styles["Heading3"]))
                story.append(
                    Paragraph(
                        _safe_para(details["description"]),
                        body_style,
                    )
                )

            security_lines = _security_lines(
                details.get("security"), global_security, components
            )
            if security_lines:
                story.append(Paragraph("Security:", styles["Heading3"]))
                for line in security_lines:
                    story.append(Paragraph(_safe_para(line), bullet_style))

            parameters = details.get("parameters", [])
            if parameters:
                story.append(Paragraph("Parameters:", styles["Heading3"]))
                for param in parameters:
                    story.append(Paragraph(_safe_para(_format_parameter(param)), bullet_style))

            request_body = details.get("requestBody", {})
            if request_body:
                required = request_body.get("required", False)
                story.append(
                    Paragraph(f"Request Body (required={required}):", styles["Heading3"])
                )
                media_types = request_body.get("content", {})
                for media_type, media_meta in media_types.items():
                    story.append(
                        Paragraph(
                            _safe_para(f"- Media Type: {media_type}"),
                            bullet_style,
                        )
                    )
                    body_schema = _resolve_schema(media_meta.get("schema", {}), components)
                    for line in _schema_lines(body_schema, indent=1):
                        story.append(Paragraph(_safe_para(line), bullet_style))
                    example_value = _extract_example(media_meta, body_schema)
                    if example_value is not None:
                        story.append(Paragraph(_safe_para("- Example:"), example_label_style))
                        story.append(
                            Preformatted(
                                _safe_para(_example_text(example_value)), example_style
                            )
                        )
                        story.append(Spacer(1, 6))
            responses = details.get("responses", {})
            if responses:
                story.append(Paragraph("Responses:", styles["Heading3"]))
                for status_code, response_meta in responses.items():
                    description = response_meta.get("description", "")
                    story.append(
                        Paragraph(
                            _safe_para(f"- {status_code}: {description}"),
                            bullet_style,
                        )
                    )
                    content = response_meta.get("content", {})
                    for media_type, media_meta in content.items():
                        story.append(
                            Paragraph(
                                _safe_para(f"- Response Media Type: {media_type}"),
                                bullet_style,
                            )
                        )
                        response_schema = _resolve_schema(
                            media_meta.get("schema", {}), components
                        )
                        for line in _schema_lines(response_schema, indent=1):
                            story.append(Paragraph(_safe_para(line), bullet_style))
                        example_value = _extract_example(media_meta, response_schema)
                        if example_value is not None:
                            story.append(Paragraph(_safe_para("- Example:"), example_label_style))
                            story.append(
                                Preformatted(
                                    _safe_para(_example_text(example_value)), example_style
                                )
                            )
                            story.append(Spacer(1, 6))

            story.append(Spacer(1, 8))
        # story.append(HRFlowable(width="100%", thickness=3, color=colors.grey))
        story.append(Spacer(1, 12))

    doc = SimpleDocTemplate(str(output_file), pagesize=A4)
    try:
        doc.build(story)
    except PermissionError:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"api-docs-{timestamp}.pdf"
        doc = SimpleDocTemplate(str(output_file), pagesize=A4)
        doc.build(story)

    print(f"Generated static PDF at: {output_file.resolve()}")


if __name__ == "__main__":
    main()
