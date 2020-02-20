from typing import Optional, Any


def extract_email_from_headers(event: dict) -> str:
    return event['headers']['email'] if 'email' in event['headers'].keys() else None


def extract_identifier_from_headers(event: dict) -> str:
    return event['headers']['exchange_identifier'] if 'exchange_identifier' in event['headers'].keys() else None


def extract_from_headers(attribute_key: str, event: dict) -> Optional[Any]:
    return event['headers'][attribute_key] if attribute_key in event['headers'].keys() else None


def extract_filename_from_headers(event: dict) -> str:
    return event['headers']['filename'] if 'filename' in event['headers'].keys() else None
