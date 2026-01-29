# import pytest (removed for standalone run)
from datetime import datetime
from zoneinfo import ZoneInfo
from app.src.models.price import Price

def test_price_timezone_aware():
    """
    Test that Price model creation uses KST timezone by default
    """
    # 1. Create a Price instance without specifying created_at/timestamp
    # Note: validation might fail if fields are missing, but we rely on defaults
    # based on price.py: asset_id, value, timestamp are fields.
    # We'll just test the default factories for now by invoking them directly or creating a model if possible.
    # Since we need asset_id, we can mock it.
    
    # Actually, let's just test the default factory logic by inspecting the field or creating a dummy.
    # But better to instantiate.
    
    import uuid
    dummy_id = uuid.uuid4()
    
    # We can check the lambda function or just create an instance if we provide required fields.
    # timestamp has a default factory in our new code?
    # Let's check the code we wrote.
    # timestamp: datetime = Field(..., default_factory=lambda: datetime.now(ZoneInfo("Asia/Seoul")))
    
    price = Price(
        asset_id=dummy_id,
        value=100.0
        # timestamp and created_at should be autofilled
    )
    
    # Check timestamp
    assert price.timestamp is not None
    assert price.timestamp.tzinfo is not None
    assert str(price.timestamp.tzinfo) == "Asia/Seoul"
    
    # Check created_at
    assert price.created_at is not None
    assert price.created_at.tzinfo is not None
    assert str(price.created_at.tzinfo) == "Asia/Seoul"

    # Verify offset (KST is UTC+9)
    # Be careful with DST but KST doesn't have DST since 1988.
    kt = datetime.now(ZoneInfo("Asia/Seoul"))
    assert kt.utcoffset().total_seconds() == 9 * 3600

if __name__ == "__main__":
    try:
        test_price_timezone_aware()
        print("Success: Price model uses Asia/Seoul timezone")
    except Exception as e:
        print(f"Failed: {e}")
        exit(1)
