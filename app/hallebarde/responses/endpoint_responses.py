from http import HTTPStatus


def generate_response(body: str or dict, status_code: HTTPStatus) -> dict:
    return {
        "isBase64Encoded": False,
        "body": body,
        "headers": None,
        "statusCode": status_code
    }
