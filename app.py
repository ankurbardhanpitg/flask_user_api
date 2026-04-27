from flask import Flask
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


if __name__ == '__main__':
    app.run(debug=True) 