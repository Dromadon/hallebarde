import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handle(event: dict, context: dict) -> dict:

    response = {"isBase64Encoded": False, "body": None, "headers": None, "statusCode": 200}
    return response
