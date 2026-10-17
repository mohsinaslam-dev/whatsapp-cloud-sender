from app import build_payload, normalize_phone


def test_normalize():
    assert normalize_phone("0300-1234567") == "923001234567"
    assert normalize_phone("+92 300 1234567") == "923001234567"
    assert normalize_phone("0044 7700 900123") == "447700900123"
    assert normalize_phone("123") is None
    assert normalize_phone(None) is None


def test_payload():
    p = build_payload("923001234567", "welcome", "en", "Ali")
    assert p["template"]["components"][0]["parameters"][0]["text"] == "Ali"
    assert "components" not in build_payload("1", "welcome", "en")["template"]
