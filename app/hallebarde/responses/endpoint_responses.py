from http import HTTPStatus
from hallebarde import config


def generate_response(body: str, status_code: HTTPStatus) -> dict:
    return {
        "isBase64Encoded": False,
        "body": body,
        "headers": {'Access-Control-Allow-Origin': get_allowed_origin()},
        "statusCode": status_code
    }


def get_allowed_origin() -> str:
    if config.ENVIRONMENT == 'dev':
        return "*"
    else:
        return 'https://'+config.WEBSITE_HOSTNAME
