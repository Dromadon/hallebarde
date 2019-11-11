import boto3
import pytest
from docker import from_env, DockerClient
from docker.models.containers import Container
from docker.models.volumes import Volume

BUCKET_NAME = f"hallebarde-storage-dev"
db_port: str = '9000'
MINIO_ACCESS_KEY = "test_access_key"
MINIO_SECRET_KEY = "test_secret_key"


@pytest.fixture(scope="module")
def get_s3_client():
    docker_client = from_env()
    minio_container_name = 'minio-test'
    minio_volume = _create_minio_volume(docker_client)
    minio_container = _run_minio_container(docker_client, minio_container_name, minio_volume)
    client = boto3.client('s3', endpoint_url='http://localhost:9000', aws_access_key_id=MINIO_ACCESS_KEY,
                          aws_secret_access_key=MINIO_SECRET_KEY)
    setup_s3_bucket(client)
    yield client
    minio_container.stop()
    minio_container.remove(v=True)
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
        command=["server", "/data"],
        detach=True,
        ports={db_port: db_port},
        volumes={minio_volume.name: {'bind': '/data', 'mode': 'rw'}},
        environment={"MINIO_ACCESS_KEY": MINIO_ACCESS_KEY, "MINIO_SECRET_KEY": MINIO_SECRET_KEY}
    )


def _create_minio_volume(docker_client: DockerClient) -> Volume:
    return docker_client.volumes.create(name="test-hallebarde")
