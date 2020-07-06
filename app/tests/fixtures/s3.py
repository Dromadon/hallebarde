import boto3
import pytest
from docker import from_env, DockerClient, errors as docker_errors
from docker.models.containers import Container
from docker.models.volumes import Volume
import hallebarde.config

BUCKET_NAME: str = f'{hallebarde.config.APPLICATION_NAME}-{hallebarde.config.ENVIRONMENT}-storage'
DB_PORT: str = '9000'
MINIO_ACCESS_KEY: str = 'test_access_key'
MINIO_SECRET_KEY: str = 'test_secret_key'


@pytest.fixture(scope='module')
def get_s3_client():
    docker_client = from_env()
    minio_container_name = 'minio-test'
    minio_volume_name = 'test-hallebarde'
    _remove_minio_container_if_running(docker_client, minio_container_name)
    minio_volume = _create_minio_volume(docker_client, minio_volume_name)
    minio_container = _run_minio_container(docker_client, minio_container_name, minio_volume)
    client = boto3.client(
        's3',
        endpoint_url=f'http://localhost:{DB_PORT}',
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY)
    setup_s3_bucket(client)
    yield client
    _stop_and_remove_container(minio_container)
    minio_volume.remove()


def setup_s3_bucket(client) -> None:
    try:
        client.create_bucket(Bucket=BUCKET_NAME)
    except Exception as e:
        print(e)


def _run_minio_container(docker_client: DockerClient, container_name: str, minio_volume: Volume) -> Container:
    return docker_client.containers.run(
        image='minio/minio',
        name=container_name,
        command=['server', '/data'],
        detach=True,
        ports={DB_PORT: DB_PORT},
        volumes={minio_volume.name: {'bind': '/data', 'mode': 'rw'}},
        environment=dict(MINIO_ACCESS_KEY=MINIO_ACCESS_KEY, MINIO_SECRET_KEY=MINIO_SECRET_KEY)
    )


def _create_minio_volume(docker_client: DockerClient, volume_name: str) -> Volume:
    return docker_client.volumes.create(name=volume_name)


def _stop_and_remove_container(container: Container) -> None:
    container.stop()
    container.remove(v=True)


def _remove_minio_container_if_running(docker_client: DockerClient, container_name: str) -> None:
    try:
        potential_old_container_running = docker_client.containers.get(container_name)
        _stop_and_remove_container(potential_old_container_running)
        print('[*] Old container found and removed')
    except docker_errors.NotFound:
        print('[*] No old container running')
