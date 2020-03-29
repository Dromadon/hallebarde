import logging

from datetime import datetime, timezone, timedelta

from hallebarde import config
from hallebarde.infrastructure import exchange_repository
from hallebarde.usecases import revoke_exchange_command_handler

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event: dict, context: dict) -> dict:
    maximum_creation_time = datetime.now(timezone.utc) - timedelta(days=config.EXPIRATION_DELAY_IN_DAYS)
    exchanges_to_revoke = exchange_repository.get_before_time(maximum_creation_time)

    for e in exchanges_to_revoke:
        revoke_exchange_command_handler.handle(e.identifier)



