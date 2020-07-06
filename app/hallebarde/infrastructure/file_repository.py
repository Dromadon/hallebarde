from typing import List, Optional

import boto3
import hallebarde.config

BUCKET_NAME = f'{hallebarde.config.APPLICATION_NAME}-{hallebarde.config.ENVIRONMENT}-storage'


def get_file(identifier: str) -> Optional[str]:
    files = _get_files(identifier)
    if files:
        return files[0]
    else:
        return None


def _get_files(identifier: str) -> Optional[List[str]]:
    client = _get_s3_client()
    files = client.list_objects(Bucket=BUCKET_NAME, Prefix=identifier)
    if 'Contents' in files.keys():
        files['Contents'].sort(key=lambda x: x['LastModified'], reverse=True)
        return [file['Key'] for file in files['Contents']]
    else:
        return None


def delete_files(identifier: str) -> None:
    client = _get_s3_client()
    files_keys = _get_files(identifier)
    if files_keys:
        client.delete_objects(Bucket=BUCKET_NAME, Delete={'Objects': [{'Key': key} for key in files_keys]})


def _get_s3_client():
    client = boto3.client('s3')
    return client
