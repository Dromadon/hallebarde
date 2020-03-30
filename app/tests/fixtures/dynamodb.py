import boto3
import pytest
from docker import from_env, DockerClient, errors as docker_errors
from docker.models.containers import Container

DB_PORT: str = '8000'
TABLE_NAME: str = 'hallebarde-dev-table'


@pytest.fixture(scope='module')
def setup_dynamodb_container(request):
    docker_client = from_env()
    dynamodb_container_name = 'dynamo-test'
    _remove_dynamo_container_if_running(docker_client, dynamodb_container_name)
    dynamodb_container = _run_dynamodb_container(docker_client, dynamodb_container_name)
    yield
    _stop_and_remove_container(dynamodb_container)


@pytest.fixture(scope='class')
def get_dynamodb_table():
    delete_dynamodb_table()
    setup_dynamodb_table()
    yield boto3.resource('dynamodb', endpoint_url=f'http://localhost:{DB_PORT}').Table(TABLE_NAME)


def setup_dynamodb_table() -> None:
    try:
        dynamodb = boto3.resource('dynamodb', endpoint_url=f'http://localhost:{DB_PORT}')
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{
                'AttributeName': 'identifier',
                'KeyType': 'HASH'
            }],
            AttributeDefinitions=[
                {'AttributeName': 'identifier',
                 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )

        table.meta.client.get_waiter('table_exists').wait(TableName=TABLE_NAME)
    except Exception as e:
        print(e)


def delete_dynamodb_table() -> None:
    try:
        dynamodb = boto3.client('dynamodb', endpoint_url=f'http://localhost:{DB_PORT}')
        dynamodb.delete_table(TableName=TABLE_NAME)
    except dynamodb.exceptions.ResourceNotFoundException:
        print("No pre-existing dynamodb table")


def _run_dynamodb_container(docker_client: DockerClient, container_name: str) -> Container:
    return docker_client.containers.run(
        image='amazon/dynamodb-local',
        name=container_name,
        detach=True,
        ports={DB_PORT: DB_PORT},
    )


def _stop_and_remove_container(container: Container) -> None:
    container.stop()
    container.remove(v=True)


def _remove_dynamo_container_if_running(docker_client: DockerClient, container_name: str) -> None:
    try:
        potential_old_container_running = docker_client.containers.get(container_name)
        _stop_and_remove_container(potential_old_container_running)
        print('[*] Old container found and removed')
    except docker_errors.NotFound:
        print('[*] No old container running')
