import boto3

import hallebarde.config
from hallebarde.domain.exchange import Exchange


def save(exchange: Exchange) -> None:
    table = _get_dynamodb_table()
    table.put_item(Item={'identifier': exchange.identifier, 'upload_token': exchange.upload_token,
                         'download_token': exchange.download_token})


def get(identifier: str) -> Exchange:
    table = _get_dynamodb_table()
    response = table.get_item(Key={'identifier': identifier})['Item']
    return Exchange(response['identifier'], response['upload_token'], response['download_token'])


def _get_dynamodb_table():
    client = boto3.resource('dynamodb')
    table = client.Table(f'hallebarde-{hallebarde.config.ENVIRONMENT}-table')
    return table
