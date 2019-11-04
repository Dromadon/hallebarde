def extract_email_from_headers(event: dict) -> str:
    return event['headers']['email'] if 'email' in event['headers'].keys() else None
