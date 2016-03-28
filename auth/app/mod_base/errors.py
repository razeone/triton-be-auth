import json


errors = {}
errors[403] = {"error": "endpoint forbidden", "errorCode": 403}
errors[404] = {"error": "endpoint not found", "errorCode": 404}
errors[405] = {"error": "method not allowed", "errorCode": 405}

errors["token_required"] = {"error": "token is required", "errorCode": 401}
errors["token_invalid"] = {"error": "token is invalid", "errorCode": 401}
errors["token_expired"] = {"error": "token has expired", "errorCode": 401}

errors["params_required"] = {"error": "params not available", "errorCode": 1011}

errors["user_not_found"] = {"error": "user not found", "errorCode": 1021}
errors["wrong_password"] = {"error": "wrong password", "errorCode": 1022}
errors["user_already_exists"] = {"error": "user already exists", "errorCode": 1023}
errors["user_not_created"] = {"error": "error creating user", "errorCode": 1024}


def error_response(error):

    response = {"success": False}
    response["error"] = errors[error]["error"]
    response["errorCode"] = errors[error]["errorCode"]

    return json.dumps(response)
