import boto3
import json

def handle(event, context):
  s3_client = boto3.client('s3')
  try:
      response = s3_client.generate_presigned_post("hallebarde-storage-dev",
                                                   "test",
                                                   Fields=None,
                                                   Conditions=None,
                                                   ExpiresIn=600)
  except ClientError as e:
      logging.error(e)
      return None

  final_response = { "isBase64Encoded": False, "body": json.dumps(response), "headers": None, "statusCode": 200 }

  # The response contains the presigned URL and required fields
  return final_response

