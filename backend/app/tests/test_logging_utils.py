from app.src.core.logging_utils import mask_email

def test_mask_email_normal():
    assert mask_email("user@example.com") == "u***@example.com"
    assert mask_email("a@b.com") == "a***@b.com"

def test_mask_email_invalid():
    assert mask_email("invalid-email") == "invalid-email"
    assert mask_email("") == ""
    assert mask_email(None) is None

def test_mask_email_long_name():
    assert mask_email("verylongusername@domain.com") == "v***@domain.com"

if __name__ == "__main__":
    test_mask_email_normal()
    test_mask_email_invalid()
    test_mask_email_long_name()
    print("All mapping tests passed!")
