def extract_email_from_headers(event: dict) -> str:
    return event['headers']['email'] if 'email' in event['headers'].keys() else None


def extract_identifier_from_headers(event: dict) -> str:
    return event['headers']['exchange_identifier'] if 'exchange_identifier' in event['headers'].keys() else None
