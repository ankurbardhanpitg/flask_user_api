from flask import Flask, jsonify, render_template_string
from openapi_spec import OPENAPI_SPEC
from routes import users_bp

app = Flask(__name__)
app.register_blueprint(users_bp)


@app.get("/openapi.json")
def openapi_json():
    return jsonify(OPENAPI_SPEC)


@app.get("/redoc")
def redoc_docs():
    return render_template_string(
        """
        <!DOCTYPE html>
        <html>
          <head>
            <title>Flask User API - ReDoc</title>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
          </head>
          <body>
            <redoc spec-url="/openapi.json"></redoc>
            <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
          </body>
        </html>
        """
    )


@app.get("/swagger")
def swagger_docs():
    return render_template_string(
        """
        <!DOCTYPE html>
        <html>
          <head>
            <title>Flask User API - Swagger UI</title>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <link
              rel="stylesheet"
              href="https://unpkg.com/swagger-ui-dist/swagger-ui.css"
            />
          </head>
          <body>
            <div id="swagger-ui"></div>
            <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
            <script>
              SwaggerUIBundle({
                url: "/openapi.json",
                dom_id: "#swagger-ui"
              });
            </script>
          </body>
        </html>
        """
    )


if __name__ == '__main__':
    app.run(debug=True) 