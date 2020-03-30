import logging

from datetime import datetime, timezone, timedelta

from hallebarde import config
from hallebarde.infrastructure import exchange_repository
from hallebarde.usecases import revoke_exchange_command_handler

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event: dict, context: dict) -> None:
    maximum_creation_time = datetime.now(timezone.utc) - timedelta(days=config.EXPIRATION_DELAY_IN_DAYS)
    logger.log(f'Revoking exchanges before {maximum_creation_time}')
    exchanges_to_revoke = exchange_repository.get_before_time(maximum_creation_time)
    logger.log(f'Revoking {len(exchanges_to_revoke)} exchanges')

    for e in exchanges_to_revoke:
        logger.log(f'Revoking exchange {e.identifier}')
        revoke_exchange_command_handler.handle(e.identifier)



