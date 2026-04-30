OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "Flask User API",
        "description": "Simple CRUD API",
        "domain": "http://127.0.0.1:5000",
        "version": "1.0.0",
    },
    "servers": [{"url": "http://127.0.0.1:5000"}],
    "tags": [{"name": "Users"}, {"name": "Companies"}],
    "paths": {
        "/users": {
            "get": {
                "tags": ["Users"],
                "summary": "List all users",
                "description": "Returns all users stored in the system.",
                "security": [{"BearerAuth": []}],
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
                "security": [{"BearerAuth": []}],
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
                "security": [{"BearerAuth": []}],
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
                "security": [{"BearerAuth": []}],
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
        "/login": {
            "post": {
                "tags": ["Users"],
                "summary": "Login user",
                "description": "Authenticates a user and returns a JWT token.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/LoginRequest"}
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Login successful",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/LoginResponse"}
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
                    "401": {
                        "description": "Invalid credentials",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/MessageResponse"}
                            }
                        },
                    },
                },
            }
        },
        "/companies": {
            "get": {
                "tags": ["Companies"],
                "summary": "List all companies",
                "description": "Returns all companies stored in the system.",
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "List of companies",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Company"},
                                }
                            }
                        },
                    }
                },
            },
            "post": {
                "tags": ["Companies"],
                "summary": "Create a company",
                "description": "Creates a new company with the given name and email.",
                "security": [{"BearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/CreateCompanyRequest"}
                        }
                    },
                },
                "responses": {
                    "201": {
                        "description": "Company created",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Company"}
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
        "/companies/{company_id}": {
            "put": {
                "tags": ["Companies"],
                "summary": "Update a company",
                "description": "Updates the company with the given id.",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "company_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/UpdateCompanyRequest"}
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Updated company",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Company"}
                            }
                        },
                    },
                    "404": {
                        "description": "Company not found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/MessageResponse"}
                            }
                        },
                    },
                },
            },
            "delete": {
                "tags": ["Companies"],
                "summary": "Delete a company",
                "description": "Deletes the company with the given id.",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "company_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Company deleted",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/MessageResponse"}
                            }
                        },
                    },
                    "404": {
                        "description": "Company not found",
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
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        },
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
            "LoginRequest": {
                "type": "object",
                "required": ["email", "password"],
                "properties": {
                    "email": {"type": "string", "example": "ankur@example.com"},
                    "password": {"type": "string", "example": "secret@123"},
                },
            },
            "LoginUser": {
                "type": "object",
                "required": ["id", "name", "email"],
                "properties": {
                    "id": {"type": "integer", "example": 1710000000000},
                    "name": {"type": "string", "example": "Ankur"},
                    "email": {"type": "string", "example": "ankur@example.com"},
                },
            },
            "LoginResponse": {
                "type": "object",
                "required": ["token", "token_type", "expires_in", "user"],
                "properties": {
                    "token": {"type": "string", "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."},
                    "token_type": {"type": "string", "example": "Bearer"},
                    "expires_in": {"type": "integer", "example": 3600},
                    "user": {"$ref": "#/components/schemas/LoginUser"},
                },
            },
            "Company": {
                "type": "object",
                "required": ["id", "name", "email"],
                "properties": {
                    "id": {"type": "integer", "example": 1710000000001},
                    "name": {"type": "string", "example": "Acme Pvt Ltd"},
                    "email": {"type": "string", "example": "hello@acme.com"},
                },
            },
            "CreateCompanyRequest": {
                "type": "object",
                "required": ["name", "email"],
                "properties": {
                    "name": {"type": "string", "example": "Acme Pvt Ltd"},
                    "email": {"type": "string", "example": "hello@acme.com"},
                },
            },
            "UpdateCompanyRequest": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "Acme Updated"},
                    "email": {"type": "string", "example": "updated@acme.com"},
                },
            },
        }
    },
}
