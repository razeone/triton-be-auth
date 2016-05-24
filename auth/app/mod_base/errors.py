import json


ERRORS = {}

# General API errors

ERRORS[400] = {
    "error": "Bad request",
    "error_code": 400
    }
ERRORS[401] = {
    "error": "Unauthorized",
    "error_code": 401
    }
ERRORS[403] = {
    "error": "Endpoint forbidden",
    "error_code": 403
    }
ERRORS[404] = {
    "error": "Endpoint not found",
    "error_code": 404
    }
ERRORS[405] = {
    "error": "Method not allowed",
    "error_code": 405
    }

# Token specific errors

ERRORS["token_required"] = {
    "error": "Token is required",
    "error_code": 401
    }
ERRORS["token_invalid"] = {
    "error": "Token is invalid",
    "error_code": 401
    }
ERRORS["token_expired"] = {
    "error": "Token has expired",
    "error_code": 401
    }

# User handling errors

ERRORS["params_required"] = {
    "error": "Params not available",
    "error_code": 400
    }
ERRORS["wrong_password"] = {
    "error": "Wrong password",
    "error_code": 400
    }
ERRORS["user_not_found"] = {
    "error": "User not found",
    "error_code": 404
    }
ERRORS["user_not_active"] = {
    "error": "User not active",
    "error_code": 404
    }
ERRORS["user_already_exists"] = {
    "error": "User already exists",
    "error_code": 409
    }
ERRORS["email_missing"] = {
    "error": "Email address is missing",
    "error_code": 422
    }
ERRORS["password_missing"] = {
    "error": "The password is missing",
    "error_code": 422
    }
ERRORS["user_not_created"] = {
    "error": "Error creating user",
    "error_code": 500
    }


def error_response(error):
    response = {"success": False}
    response["error"] = ERRORS[error]["error"]
    return json.dumps(response), ERRORS[error]["error_code"]
