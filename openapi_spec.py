OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "Flask User API",
        "description": "Simple CRUD API for users",
        "version": "1.0.0",
    },
    "servers": [{"url": "/"}],
    "tags": [{"name": "Users"}],
    "paths": {
        "/users": {
            "get": {
                "tags": ["Users"],
                "summary": "List all users",
                "description": "Returns all users stored in the system.",
                "responses": {
                    "200": {
                        "description": "List of users",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/User"},
                                }
                            }
                        },
                    }
                },
            },
            "post": {
                "tags": ["Users"],
                "summary": "Create a user",
                "description": "Creates a new user with the given name, email and password.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/CreateUserRequest"}
                        }
                    },
                },
                "responses": {
                    "201": {
                        "description": "User created",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    },
                    "400": {
                        "description": "Invalid request body",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/MessageResponse"}
                            }
                        },
                    },
                },
            },
        },
        "/users/{user_id}": {
            "put": {
                "tags": ["Users"],
                "summary": "Update a user",
                "description": "Updates the user with the given id.",
                "parameters": [
                    {
                        "name": "user_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/UpdateUserRequest"}
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Updated user",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    },
                    "404": {
                        "description": "User not found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/MessageResponse"}
                            }
                        },
                    },
                },
            },
            "delete": {
                "tags": ["Users"],
                "summary": "Delete a user",
                "description": "Deletes the user with the given id.",
                "parameters": [
                    {
                        "name": "user_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "User deleted",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/MessageResponse"}
                            }
                        },
                    },
                    "404": {
                        "description": "User not found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/MessageResponse"}
                            }
                        },
                    },
                },
            },
        },
    },
    "components": {
        "schemas": {
            "User": {
                "type": "object",
                "required": ["id", "name", "email", "password"],
                "properties": {
                    "id": {"type": "integer", "example": 1710000000000},
                    "name": {"type": "string", "example": "Ankur"},
                    "email": {"type": "string", "example": "ankur@example.com"},
                    "password": {"type": "string", "example": "secret@123"},
                },
            },
            "CreateUserRequest": {
                "type": "object",
                "required": ["name", "email", "password"],
                "properties": {
                    "name": {"type": "string", "example": "Ankur"},
                    "email": {"type": "string", "example": "ankur@example.com"},
                    "password": {"type": "string", "example": "secret@123"},
                },
            },
            "UpdateUserRequest": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "Updated Name"},
                    "email": {"type": "string", "example": "updated@example.com"},
                    "password": {"type": "string", "example": "updated@123"},
                },
            },
            "MessageResponse": {
                "type": "object",
                "required": ["message"],
                "properties": {"message": {"type": "string", "example": "User not found"}},
            },
        }
    },
}
