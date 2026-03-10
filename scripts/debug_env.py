"""
Debug script — prints env vars as Python sees them before pytest runs.
Secrets are masked (first 4 chars only). Safe to run in CI.
"""
import os


def mask(value: str, show: int = 4) -> str:
    if not value:
        return "<empty>"
    return value[:show] + "***" if len(value) > show else value


vars_to_check = [
    ("USER_EMAIL",      False),
    ("PASSWORD",        True),
    ("IDS_URL",         False),
    ("AUTH_TOKEN",      True),
    ("USER_EMAIL_POOL", False),
    ("ENV_NAME",        False),
    ("CI",              False),
]

print("=== [DEBUG] ENV VARS AS SEEN BY PYTHON ===")
for name, secret in vars_to_check:
    raw = os.getenv(name, "")
    if secret:
        display = f"{mask(raw)} (len={len(raw)})"
    else:
        display = raw if raw else "<not set>"
    print(f"  {name:<20}: {display}")
print("==========================================")
