from hallebarde.infrastructure import exchange_repository, file_repository


def revoke_an_exchange_by_its_identifier(identifier: str) -> None:
    file_repository.delete_files(identifier)
    exchange_repository.delete(identifier)
