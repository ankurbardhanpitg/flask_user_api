from flask import Flask, jsonify, render_template_string, send_from_directory
from openapi_spec import OPENAPI_SPEC
from pam_project.pam_project_spec import PAM_PROJECT_SPEC
from routes import users_bp, companies_bp

app = Flask(__name__)
app.register_blueprint(users_bp)
app.register_blueprint(companies_bp)


@app.get("/core_lib/<path:filename>")
def core_lib_static(filename: str):
    return send_from_directory("core_lib", filename)

@app.get("/pam_project.json")
def pam_project_json():
    return jsonify(PAM_PROJECT_SPEC)


@app.get("/pam_project/redoc")
def pam_project_redoc():
    return render_template_string(
        """
        <!DOCTYPE html>
        <html>
          <head>
            <title>PAM Project - ReDoc</title>
            <meta charset="utf-8" />  
            <meta name="viewport" content="width=device-width, initial-scale=1" />
          </head>
          <body>
            <redoc spec-url="/pam_project.json"></redoc>
            <script src="/core_lib/redoc.standalone.js"></script>
          </body>
        </html>
        """
    )

@app.get("/pam_project/swagger")
def pam_project_swagger():
    return render_template_string(
        """
        <!DOCTYPE html>
        <html>
          <head>
            <title>PAM Project - Swagger</title>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
          </head>
          <body>
            <div id="swagger-ui"></div>
            <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
            <script>
              SwaggerUIBundle({
                url: "/pam_project.json",
                dom_id: "#swagger-ui"
              });
            </script>
          </body>
        </html>
        """
    )


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
            <script src="/core_lib/redoc.standalone.js"></script>
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