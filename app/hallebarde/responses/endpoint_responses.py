from http import HTTPStatus


def generate_response(body: str, status_code: HTTPStatus) -> dict:
    return {
        "isBase64Encoded": False,
        "body": body,
        "headers": None,
        "statusCode": status_code
    }
