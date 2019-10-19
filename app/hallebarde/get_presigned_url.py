import json
import logging
from typing import Optional

import boto3
from botocore.exceptions import ClientError


def handle(event: dict, context) -> Optional[dict]:
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_post(
            "hallebarde-storage-dev",
            "test",
            Fields=None,
            Conditions=None,
            ExpiresIn=600
        )
    except ClientError as e:
        logging.error(e)
        return None

    return {
        "isBase64Encoded": False,
        "body": json.dumps(response),
        "headers": None,
        "statusCode": 200
    }
