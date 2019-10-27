from unittest import TestCase
from unittest.mock import patch

import boto3
from docker import from_env, DockerClient
from docker.models.containers import Container

from hallebarde.domain.exchange import Exchange
from hallebarde.infrastructure import exchange_repository

TABLE_NAME = f'hallebarde-dev-table'


class TestExchangeRepository(TestCase):
    dynamodb_container: Container = None
    db_port: str = '8000'

    @classmethod
    def setUpClass(cls) -> None:
        cls.docker_client = from_env()
        cls.dynamodb_container_name = 'dynamo-test'
        cls.dynamodb_container = cls._run_dynamodb_container(cls.docker_client, cls.dynamodb_container_name)
        cls.setup_dynamodb_table()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.dynamodb_container.stop()
        cls.dynamodb_container.remove(v=True)

    @classmethod
    def setup_dynamodb_table(cls) -> None:
        try:
            dynamodb = boto3.resource('dynamodb', endpoint_url=f'http://localhost:{cls.db_port}')
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
            print(table.attribute_definitions)
        except Exception as e:
            print(e)
            cls.tearDownClass()

    @patch('hallebarde.infrastructure.exchange_repository._get_dynamodb_table')
    def test_save_should_create_readable_item(self, mock_boto_resource):
        # Given
        mock_boto_resource.return_value = boto3.resource('dynamodb',
                                                         endpoint_url=f'http://localhost:{self.db_port}').Table(
            TABLE_NAME)
        expected_exchange = Exchange('06d027bf-3783-4b6a-bec4-8888d8b26fb4',
                                     '9WsE02XcMAekmjKHoj9Zq7_uVqc8dVz1Fq8czbZOq_Y',
                                     '2yOdhL1NM5lyX7Mt8pHVYfkE51UkoSuGUrv6z4OT-c4')

        # When
        exchange_repository.save(expected_exchange)

        # Then
        actual_exchange = exchange_repository.get('06d027bf-3783-4b6a-bec4-8888d8b26fb4')
        assert actual_exchange == expected_exchange

    @classmethod
    def _run_dynamodb_container(cls, docker_client: DockerClient, container_name: str) -> Container:
        return docker_client.containers.run(
            image='amazon/dynamodb-local',
            name=container_name,
            detach=True,
            ports={cls.db_port: cls.db_port},
        )
