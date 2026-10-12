import re

EMAIL = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
PHONE = r"(?<!\d)(?:\+?91[\s-]?)?[6-9]\d{9}(?!\d)"
AADHAAR = r"(?<!\d)\d{4}[\s-]?\d{4}[\s-]?\d{4}(?!\d)"
NAME_FIELD = r"(?im)(\bName\s*:\s*)[^\r\n]+"
NAME_MSG = r"(?i:\bmy name is\s+)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)"

def redact_pii(text):
    counts = {}
    for label, pat in [("Email", EMAIL), ("Phone", PHONE), ("Aadhaar-like", AADHAAR)]:
        text, n = re.subn(pat, "[REDACTED]", text)
        counts[label] = n
    text, n = re.subn(NAME_FIELD, lambda m: m.group(1) + "[REDACTED]", text)
    counts["Name field"] = n
    text, n = re.subn(NAME_MSG, lambda m: m.group(0).replace(m.group(1), "[REDACTED]"), text)
    counts["Name in message"] = n
    return text, counts
