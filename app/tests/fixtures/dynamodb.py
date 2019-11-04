import boto3
import pytest
from docker import from_env, DockerClient
from docker.models.containers import Container

TABLE_NAME = f"hallebarde-dev-table"
db_port: str = '8000'


@pytest.fixture(scope="module")
def get_dynamodb_table():
    docker_client = from_env()
    dynamodb_container_name = 'dynamo-test'
    dynamodb_container = _run_dynamodb_container(docker_client, dynamodb_container_name)
    setup_dynamodb_table()
    yield boto3.resource('dynamodb',
                         endpoint_url=f'http://localhost:{db_port}').Table(TABLE_NAME)
    dynamodb_container.stop()
    dynamodb_container.remove(v=True)


def setup_dynamodb_table() -> None:
    try:
        dynamodb = boto3.resource('dynamodb', endpoint_url=f'http://localhost:{db_port}')
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'identifier',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'identifier',
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )

        table.meta.client.get_waiter('table_exists').wait(TableName=TABLE_NAME)
    except Exception as e:
        print(e)


def _run_dynamodb_container(docker_client: DockerClient, container_name: str) -> Container:
    return docker_client.containers.run(
        image='amazon/dynamodb-local',
        name=container_name,
        detach=True,
        ports={db_port: db_port},
    )
