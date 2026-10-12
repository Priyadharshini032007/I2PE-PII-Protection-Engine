import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from pii_engine import redact_pii

def test_email():
    out, c = redact_pii("mail a@b.com")
    assert "a@b.com" not in out and c["Email"] == 1

def test_phone():
    out, c = redact_pii("call 9876543210")
    assert "9876543210" not in out and c["Phone"] == 1

def test_aadhaar():
    out, c = redact_pii("id 1234 5678 9012")
    assert "1234 5678 9012" not in out and c["Aadhaar-like"] == 1

def test_name_field():
    out, _ = redact_pii("Name: Priya Kumar")
    assert out == "Name: [REDACTED]"

def test_name_in_message():
    out, _ = redact_pii("my name is Priya Kumar and I need help")
    assert out == "my name is [REDACTED] and I need help"

def test_no_pii():
    assert redact_pii("Hello world")[0] == "Hello world"
