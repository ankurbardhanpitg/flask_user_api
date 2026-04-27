from flask import Flask, render_template_string
from flasgger import Swagger
from routes import users_bp

app = Flask(__name__)
swagger = Swagger(
    app,
    template={
        "swagger": "2.0",
        "info": {
            "title": "Flask User API",
            "description": "Simple CRUD API for users",
            "version": "1.0.0",
        },
    },
)
app.register_blueprint(users_bp)


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
            <redoc spec-url="/apispec_1.json"></redoc>
            <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
          </body>
        </html>
        """
    )


if __name__ == '__main__':
    app.run(debug=True) 