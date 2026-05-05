PAM_PROJECT_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "PAM Project API",
        "description": (
            "This is the API for the PAM Project. These apis are used to fetch the PAM Project and several essentials information which are needed to be displayed in the PAM Project."
        ),
        "version": "1.0.0",
    },
    "servers": [{"url": "https://192.168.1.209", "description": "PAM appliance (example)"}],
    "tags": [
        {"name": "SPF", "description": "SPF.Util JSON-RPC-style module calls"},
        {"name": "resource", "description": "Privileged credential vault resource endpoints"},
    ],
    "paths": {
        "/SPF.Util": {
            "post": {
                "tags": ["SPF"],
                "summary": "Login",
                "description": (
                    "This api is used to login to the PAM Project. In the response, you will get the user information, identity, and auth token."
                ),
                "security": [{}, {"PumRestAuthCookie": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/SpfCallModuleRequest"},
                            "examples": {
                                "authLogin": {
                                    "summary": "auth.login via callModuleEx",
                                    "value": {
                                        "method": "callModuleEx",
                                        "params": {
                                            "pkt": {
                                                "module": "auth",
                                                "method": "login",
                                                "Credentials": {
                                                    "name": "admin",
                                                    "passwd": "<password>",
                                                },
                                            },
                                            "svc_name": None,
                                        },
                                    },
                                },
                                "getUserSecAuthMethods": {
                                    "summary": "auth.getUserSecAuthMethods (callModule + uid)",
                                    "value": {
                                        "method": "callModule",
                                        "params": {
                                            "pkt": {
                                                "module": "auth",
                                                "method": "getUserSecAuthMethods",
                                                "uid": "<pum_rest_auth / session blob>",
                                            },
                                            "svc_name": None,
                                        },
                                    },
                                },
                            },
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": (
                            "JSON result. `status` is 0 on success; non-zero typically "
                            "indicates an error (exact semantics depend on product version `vrm`)."
                        ),
                        "content": {
                            "application/json": {
                                "schema": {
                                    "oneOf": [
                                        {"$ref": "#/components/schemas/PamCallModuleSuccess"},
                                        {"$ref": "#/components/schemas/PamCallModuleError"},
                                    ]
                                },
                                "examples": {
                                    "authenticated": {
                                        "summary": "Successful login (status 0)",
                                        "value": {
                                            "vrm": "4.6.0",
                                            "message": (
                                                "User admin@pam02.pitg.site(192.168.1.135) "
                                                "successfully authenticated"
                                            ),
                                            "status": 0,
                                            "svc": "pam02.pitg.site",
                                            "User": {
                                                "name": "admin",
                                                "spf_auth_type": 100,
                                                "ACT_LAST_SUCC_LOGON": {"value": 1777876750},
                                                "ACT_LAST_UNSUCC_LOGON": {"value": 1777876813},
                                                "ACT_NUM_BADLOGONS": {"value": 1},
                                            },
                                            "Identity": {
                                                "content": "<base64-encoded identity blob>"
                                            },
                                            "AuthToken": {
                                                "name": "admin",
                                                "token_id": None,
                                                "token_vault_id": None,
                                                "spf_auth_type": 100,
                                                "inactive": 1800,
                                                "tstamp": 1777876859,
                                                "remote_host": "192.168.1.135",
                                                "peer_host": "pam02.pitg.site",
                                                "User": {
                                                    "name": "admin",
                                                    "spf_auth_type": 100,
                                                    "ACT_COMMENT": {
                                                        "value": "Administration Account"
                                                    },
                                                    "PWD_MAXAGE": {"value": False},
                                                    "ACT_UNUSED_LIMIT": {"value": False},
                                                    "ACT_UNUSED_DELETE": {"value": False},
                                                    "ACT_CREATED": {"value": 1773254972},
                                                    "ACT_PASSWD": {
                                                        "value": (
                                                            "SHA256#/WWnhOA4R5SGotJDzsgDx+PzvPj"
                                                            "ocKRlHk8WmIZlVA="
                                                        )
                                                    },
                                                    "PWD_LAST_CHG": {"value": 1773255072},
                                                    "PWD_HISTORY": {
                                                        "value": {
                                                            "SHA256#/WWnhOA4R5SGotJDzsgDx+PzvPj"
                                                            "ocKRlHk8WmIZlVA=": {}
                                                        }
                                                    },
                                                    "PWD_EXPIRED": {"value": False},
                                                    "ACT_LAST_SUCC_LOGON": {
                                                        "value": 1777876750
                                                    },
                                                    "ACT_LAST_UNSUCC_LOGON": {
                                                        "value": 1777876813
                                                    },
                                                    "ACT_NUM_BADLOGONS": {"value": 1},
                                                    "ACT_MAPS": {"value": {}},
                                                },
                                                "PCD": {
                                                    "ct": "<base64>",
                                                    "iv": "<base64>",
                                                    "cipher_type": "aes-256-cbc",
                                                    "ek": {
                                                        "id": "<base64>",
                                                        "ek": "<base64 wrapped key>",
                                                    },
                                                },
                                                "Role": [
                                                    {"mod": "prvcrdvlt", "role": "*"},
                                                    {"mod": "taskmanager", "role": "admin"},
                                                    {
                                                        "mod": "userreqdashboard",
                                                        "role": "admin",
                                                    },
                                                    {"role": "*"},
                                                    {"role": "admin"},
                                                ],
                                            },
                                        },
                                    }
                                },
                            }
                        },
                    }
                },
            }
        },
        "/rest/prvcrdvlt/Resources": {
            "get": {
                "tags": ["resource"],
                "summary": "List vault resources",
                "description": (
                    "This api is used to fetch the list of resources "
                    "session. Requires the `pum_rest_auth` cookie."
                ),
                "security": [{"PumRestAuthCookie": []}],
                "responses": {
                    "200": {
                        "description": "Resources returned successfully.",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/PrvcrdvltResourcesResponse"},
                                "examples": {
                                    "resourcesList": {
                                        "summary": "Example resources payload",
                                        "value": {
                                            "vrm": "4.6.0",
                                            "status": 200,
                                            "message": "All the resources are returned successfully.",
                                            "svc": "pam02.pitg.site",
                                            "Vault": [
                                                {
                                                    "id": "a2808230-3c96-11f1-9377-2b26fe29c1ca",
                                                    "name": "192.168.1.216",
                                                    "type": "ssh",
                                                    "path": 0,
                                                    "profile": 101,
                                                    "resource_profile_name": "SSH",
                                                    "passwordManaged": 0,
                                                    "enable_discovery": 0,
                                                    "credentials": 1,
                                                    "ACL": {"Role": {}},
                                                }
                                            ],
                                        },
                                    }
                                },
                            }
                        },
                    },
                    "401": {
                        "description": "Missing, expired, or invalid `pum_rest_auth` cookie.",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/PrvcrdvltErrorResponse"}
                            }
                        },
                    },
                },
            }
        },
    },
    "components": {
        "securitySchemes": {
            "PumRestAuthCookie": {
                "type": "apiKey",
                "in": "cookie",
                "name": "pum_rest_auth",
                "description": "Session cookie set by the PAM web UI after sign-in.",
            }
        },
        "schemas": {
            "SpfCallModuleRequest": {
                "type": "object",
                "required": ["method", "params"],
                "properties": {
                    "method": {
                        "type": "string",
                        "enum": ["callModule", "callModuleEx"],
                        "description": (
                            "`callModule` — dispatch with `pkt.uid` (session blob). "
                            "`callModuleEx` — extended dispatch (e.g. `pkt.Credentials` for "
                            "`auth.login`)."
                        ),
                    },
                    "params": {"$ref": "#/components/schemas/SpfCallModuleParams"},
                },
            },
            "SpfCallModuleParams": {
                "type": "object",
                "required": ["pkt"],
                "properties": {
                    "pkt": {"$ref": "#/components/schemas/SpfCallModulePkt"},
                    "svc_name": {
                        "type": "string",
                        "nullable": True,
                        "description": "Optional service name; null in the captured call.",
                    },
                },
            },
            "SpfCallModulePkt": {
                "oneOf": [
                    {"$ref": "#/components/schemas/SpfCallModulePktWithUid"},
                    {"$ref": "#/components/schemas/SpfCallModulePktWithCredentials"},
                ],
                "description": (
                    "Module call payload. Either include `uid` (typical `callModule` follow-up) "
                    "or `Credentials` (typical `callModuleEx` + `auth.login`)."
                ),
            },
            "SpfCallModulePktWithUid": {
                "type": "object",
                "required": ["module", "method", "uid"],
                "properties": {
                    "module": {
                        "type": "string",
                        "example": "auth",
                        "description": "Backend module name.",
                    },
                    "method": {
                        "type": "string",
                        "example": "getUserSecAuthMethods",
                        "description": "Method on the module.",
                    },
                    "uid": {
                        "type": "string",
                        "description": (
                            "Opaque encoded user/session identifier (often mirrors or derives "
                            "from cookie state)."
                        ),
                    },
                },
                "additionalProperties": True,
            },
            "SpfCallModulePktWithCredentials": {
                "type": "object",
                "required": ["module", "method", "Credentials"],
                "properties": {
                    "module": {
                        "type": "string",
                        "example": "auth",
                        "description": "Backend module name.",
                    },
                    "method": {
                        "type": "string",
                        "example": "login",
                        "description": "Method on the module (e.g. `login`).",
                    },
                    "Credentials": {
                        "$ref": "#/components/schemas/PamLoginCredentials",
                        "description": "Account name and password for password-based login.",
                    },
                },
                "additionalProperties": True,
            },
            "PamLoginCredentials": {
                "type": "object",
                "required": ["name", "passwd"],
                "properties": {
                    "name": {"type": "string", "description": "Account login name."},
                    "passwd": {
                        "type": "string",
                        "format": "password",
                        "description": "Plain-text password (use TLS to the appliance).",
                    },
                },
            },
            "PamWrappedAttribute": {
                "type": "object",
                "description": "PAM attribute wrapper; inner `value` type varies by field.",
                "properties": {
                    "value": {
                        "description": "Scalar or structured value depending on attribute name.",
                    }
                },
                "additionalProperties": True,
            },
            "PamUserSummary": {
                "type": "object",
                "description": "Top-level `User` object returned on success.",
                "properties": {
                    "name": {"type": "string"},
                    "spf_auth_type": {"type": "integer"},
                    "ACT_LAST_SUCC_LOGON": {"$ref": "#/components/schemas/PamWrappedAttribute"},
                    "ACT_LAST_UNSUCC_LOGON": {"$ref": "#/components/schemas/PamWrappedAttribute"},
                    "ACT_NUM_BADLOGONS": {"$ref": "#/components/schemas/PamWrappedAttribute"},
                },
                "additionalProperties": True,
            },
            "PamIdentity": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Base64-encoded identity / ticket material.",
                    }
                },
                "additionalProperties": True,
            },
            "PamPcdEk": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "ek": {"type": "string", "description": "Wrapped key material (base64)."},
                },
                "additionalProperties": True,
            },
            "PamPcd": {
                "type": "object",
                "description": "Per-connection crypto descriptor for the session.",
                "properties": {
                    "ct": {"type": "string"},
                    "iv": {"type": "string"},
                    "cipher_type": {"type": "string", "example": "aes-256-cbc"},
                    "ek": {"$ref": "#/components/schemas/PamPcdEk"},
                },
                "additionalProperties": True,
            },
            "PamRoleEntry": {
                "type": "object",
                "properties": {
                    "mod": {"type": "string", "description": "Module name when scoped."},
                    "role": {"type": "string"},
                },
                "additionalProperties": True,
            },
            "PamAuthTokenUser": {
                "type": "object",
                "description": "Expanded user record nested under `AuthToken.User`.",
                "properties": {
                    "name": {"type": "string"},
                    "spf_auth_type": {"type": "integer"},
                    "ACT_COMMENT": {"$ref": "#/components/schemas/PamWrappedAttribute"},
                    "PWD_MAXAGE": {"$ref": "#/components/schemas/PamWrappedAttribute"},
                    "ACT_UNUSED_LIMIT": {"$ref": "#/components/schemas/PamWrappedAttribute"},
                    "ACT_UNUSED_DELETE": {"$ref": "#/components/schemas/PamWrappedAttribute"},
                    "ACT_CREATED": {"$ref": "#/components/schemas/PamWrappedAttribute"},
                    "ACT_PASSWD": {"$ref": "#/components/schemas/PamWrappedAttribute"},
                    "PWD_LAST_CHG": {"$ref": "#/components/schemas/PamWrappedAttribute"},
                    "PWD_HISTORY": {"$ref": "#/components/schemas/PamWrappedAttribute"},
                    "PWD_EXPIRED": {"$ref": "#/components/schemas/PamWrappedAttribute"},
                    "ACT_LAST_SUCC_LOGON": {"$ref": "#/components/schemas/PamWrappedAttribute"},
                    "ACT_LAST_UNSUCC_LOGON": {"$ref": "#/components/schemas/PamWrappedAttribute"},
                    "ACT_NUM_BADLOGONS": {"$ref": "#/components/schemas/PamWrappedAttribute"},
                    "ACT_MAPS": {"$ref": "#/components/schemas/PamWrappedAttribute"},
                },
                "additionalProperties": True,
            },
            "PamAuthToken": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "token_id": {"type": "string", "nullable": True},
                    "token_vault_id": {"type": "string", "nullable": True},
                    "spf_auth_type": {"type": "integer"},
                    "inactive": {
                        "type": "integer",
                        "description": "Inactivity timeout in seconds (e.g. 1800).",
                    },
                    "tstamp": {"type": "integer", "description": "Server timestamp associated with the token."},
                    "remote_host": {"type": "string"},
                    "peer_host": {"type": "string"},
                    "User": {"$ref": "#/components/schemas/PamAuthTokenUser"},
                    "PCD": {"$ref": "#/components/schemas/PamPcd"},
                    "Role": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/PamRoleEntry"},
                    },
                },
                "additionalProperties": True,
            },
            "PamCallModuleSuccess": {
                "type": "object",
                "required": ["vrm", "message", "status"],
                "properties": {
                    "vrm": {"type": "string", "description": "Product / API version string."},
                    "message": {"type": "string"},
                    "status": {"type": "integer", "enum": [0], "description": "0 indicates success."},
                    "svc": {"type": "string", "description": "Logical service / appliance id."},
                    "User": {"$ref": "#/components/schemas/PamUserSummary"},
                    "Identity": {"$ref": "#/components/schemas/PamIdentity"},
                    "AuthToken": {"$ref": "#/components/schemas/PamAuthToken"},
                },
                "additionalProperties": True,
            },
            "PamCallModuleError": {
                "type": "object",
                "required": ["status"],
                "properties": {
                    "vrm": {"type": "string"},
                    "message": {"type": "string"},
                    "status": {
                        "type": "integer",
                        "not": {"enum": [0]},
                        "description": "Non-zero when the call failed.",
                    },
                },
                "additionalProperties": True,
            },
            "PrvcrdvltResource": {
                "type": "object",
                "description": "Single resource entry from the privileged credential vault API.",
                "required": [
                    "id",
                    "name",
                    "type",
                    "path",
                    "profile",
                    "resource_profile_name",
                    "enable_discovery",
                    "credentials",
                    "ACL",
                ],
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "type": {"type": "string", "description": "Resource type (e.g. ssh, windows, SSO, ldap, database)."},
                    "path": {"type": "integer"},
                    "profile": {"type": "integer"},
                    "resource_profile_name": {"type": "string"},
                    "passwordManaged": {"type": "integer", "description": "Password management flag when present."},
                    "enable_discovery": {"type": "integer"},
                    "credentials": {"type": "integer"},
                    "domain": {"type": "string", "description": "Domain resource id when present (e.g. windows resource)."},
                    "cred": {"type": "string", "description": "Credential id when present (e.g. ldap resource)."},
                    "ACL": {"$ref": "#/components/schemas/PrvcrdvltAcl"},
                },
                "additionalProperties": True,
            },
            "PrvcrdvltAcl": {
                "type": "object",
                "properties": {
                    "Role": {
                        "type": "object",
                        "description": "Role mapping object; may be empty in list responses.",
                        "additionalProperties": True,
                    }
                },
                "additionalProperties": True,
            },
            "PrvcrdvltResourcesResponse": {
                "type": "object",
                "required": ["vrm", "status", "message", "svc", "Vault"],
                "properties": {
                    "vrm": {"type": "string"},
                    "message": {"type": "string"},
                    "status": {"type": "integer", "enum": [200]},
                    "svc": {"type": "string"},
                    "Vault": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/PrvcrdvltResource"},
                    },
                },
                "additionalProperties": True,
            },
            "PrvcrdvltErrorResponse": {
                "type": "object",
                "required": ["status"],
                "properties": {
                    "vrm": {"type": "string"},
                    "message": {"type": "string"},
                    "status": {"type": "integer"},
                },
                "additionalProperties": True,
            },
        },
    },
}
