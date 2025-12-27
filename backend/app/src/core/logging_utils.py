import re

def mask_email(email: str) -> str:
    """
    이메일 주소를 마스킹 처리합니다.
    예: user@example.com -> u***@example.com
    """
    if not email or "@" not in email:
        return email
    
    user_part, domain_part = email.split("@", 1)
    if not user_part:
        return email
    
    masked_user = user_part[0] + "***"
    return f"{masked_user}@{domain_part}"
