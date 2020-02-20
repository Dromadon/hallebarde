from typing import Optional, Any


def extract_from_headers(attribute_key: str, event: dict) -> Optional[Any]:
    return event['headers'][attribute_key] if attribute_key in event['headers'].keys() else None
