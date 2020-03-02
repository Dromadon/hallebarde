import logging
from typing import List, Optional

import boto3
from boto3.dynamodb.conditions import Attr
from boto3.dynamodb.table import TableResource

import hallebarde.config
from hallebarde.domain.exchange import Exchange

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def save(exchange: Exchange) -> None:
    table = _get_dynamodb_table()
    table.put_item(Item=exchange.__dict__)


def get(identifier: str) -> Optional[Exchange]:
    table = _get_dynamodb_table()
    response = table.get_item(Key={'identifier': identifier})
    return _map_exchange_from_item(response['Item']) if 'Item' in response.keys() else None


def get_account_exchanges(sub: str) -> List[Exchange]:
    table = _get_dynamodb_table()
    response = table.scan(
        FilterExpression=Attr('sub').eq(sub)
    )
    return [_map_exchange_from_item(item) for item in response['Items']]


def get_by_upload_token(upload_token: str) -> Optional[Exchange]:
    table = _get_dynamodb_table()
    response = table.scan(
        FilterExpression=Attr('upload_token').eq(upload_token)
    )
    items: Optional[list] = response['Items']
    return _map_exchange_from_item(items[0]) if items else None


def delete(identifier: str) -> None:
    table = _get_dynamodb_table()
    table.delete_item(Key={'identifier': identifier})


def revoke_upload(identifier: str) -> None:
    table = _get_dynamodb_table()
    table.update_item(Key={'identifier': identifier},
                      UpdateExpression="set revoked_upload = :r",
                      ExpressionAttributeValues={
                          ':r': True})
    return None


def get_identifier_from_token(upload_token: Optional[str] = None,
                              download_token: Optional[str] = None) -> Optional[str]:
    table = _get_dynamodb_table()
    if upload_token:
        logger.info(f'Getting identifier from upload token: {upload_token}')
        attribute = 'upload_token'
        token = upload_token
    elif download_token:
        attribute = 'download_token'
        token = download_token
    else:
        return None

    response = table.scan(FilterExpression=Attr(attribute).eq(token))
    logger.info(f'Response from dynamodb: {response}')

    return _extract_identifier_from_response(response)


def _get_dynamodb_table() -> TableResource:
    resource = boto3.resource('dynamodb')
    table = resource.Table(f'hallebarde-{hallebarde.config.ENVIRONMENT}-table')
    return table


def _map_exchange_from_item(item):
    return Exchange(item['identifier'], item['sub'], item['upload_token'], item['download_token'],
                    item['revoked_upload'])


def _extract_identifier_from_response(response) -> Optional[str]:
    if len(response['Items']) == 1:
        return response['Items'][0]['identifier']
    else:
        return None
