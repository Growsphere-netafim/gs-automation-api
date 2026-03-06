"""
Script to test token acquisition
"""
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from core.token_manager import TokenManager
from config.settings import get_settings
from requests import Session

def main():
    settings = get_settings()
    session = Session()
    session.verify = False
    
    print(f"Attempting to get token for: {settings.USER_EMAIL}")
    print(f"IDS URL: {settings.IDS_URL}")
    
    try:
        token_manager = TokenManager(session, settings.USER_EMAIL, settings)
        token = token_manager.get_token()
        print("\nSUCCESS! Token obtained:")
        print(f"{token[:20]}...{token[-20:]}")
        return token
    except Exception as e:
        print(f"\nFAILED to get token: {e}")
        return None

if __name__ == "__main__":
    main()
