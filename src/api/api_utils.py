from .api_key import generate_api_key


def validate_response(response_json):
    if isinstance(response_json, dict) and response_json.get("error"):
        error_code = response_json["error"]["code"]
        if error_code == "quota_exceeded":
            generate_api_key()
        else:
            raise TypeError(f"Request Error: {error_code}")


def read_api_key():
    with open("api.key") as f:
        key = f.read()
    return key
