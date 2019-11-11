from typing import Optional, Any
import jwt


def extract_from_headers(attribute_key: str, event: dict) -> Optional[Any]:
    return event['headers'][attribute_key] if attribute_key in event['headers'].keys() else None


def extract_sub_from_jwt(jwt_token: str) -> Optional[str]:
    token_data = jwt.decode(jwt_token, verify=False)
    return token_data['sub']
