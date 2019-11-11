from typing import List

import pytest

from hallebarde.domain.exchange import Exchange

exchange1 = Exchange('e68faee7-753e-49a6-a372-dc1cdc0dae03', 'sub',
                     '-j1WjK_KnE8cQOVCYOb9WTM-qKLhyfp-DdVXSAjJthE', 'ccgxa2udCPYcw9T1mKAXud2hHgOX_14q__KVK7p910E')
exchange2 = Exchange('224c74ed-eeac-47d2-b8fe-165a0e30815f', 'sub',
                     '9WsE02XcMAekmjKHoj9Zq7_uVqc8dVz1Fq8czbZOq_Y', '2yOdhL1NM5lyX7Mt8pHVYfkE51UkoSuGUrv6z4OT-c4')
exchange3 = Exchange('97de5cec-33e6-49ae-8ee8-8865ce357625', 'adifferentsub',
                     'tKcYqm-c0FujZrstLkcwLty_lSVAYxtfPHkRJmwmoxw', 'DEXeS6gfdhXOmj9KqmAGvqvFJUc8GCk_ZB4AU_f5Rag')


@pytest.fixture
def an_exchange() -> Exchange:
    return exchange1


@pytest.fixture
def an_exchange_with_different_sub() -> Exchange:
    return exchange3


@pytest.fixture
def two_exchanges_with_same_sub() -> List[Exchange]:
    return [exchange1, exchange2]
