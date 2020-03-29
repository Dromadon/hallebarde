from hallebarde.infrastructure import exchange_repository, file_repository


def handle(identifier: str) -> None:
    file_repository.delete_files(identifier)
    exchange_repository.delete(identifier)
