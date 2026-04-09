"""
Token Manager - Smart token caching and management
Prevents unnecessary authentication requests
"""
import logging
import time
import jwt
from typing import Optional, Dict
from datetime import datetime, timedelta
from threading import Lock
from requests import Session

from core.auth import OAuth2Client
from config.settings import Settings


class TokenManager:
    """
    Manages access tokens with automatic refresh and caching
    Thread-safe for parallel test execution
    """
    
    # Class-level cache shared across all instances
    _token_cache: Dict[str, Dict] = {}
    _cache_lock = Lock()
    
    def __init__(self, session: Session, user_email: str, settings: Settings):
        self.session = session
        self.user_email = user_email
        self.settings = settings
        self.oauth_client = OAuth2Client(session, user_email, settings)
        # Cache key includes IDS URL so different environments don't share tokens
        ids_host = settings.IDS_URL.rstrip("/").split("/")[-1] if settings.IDS_URL else "default"
        self._cache_key = f"{user_email}::{ids_host}"
    
    def get_token(self) -> str:
        """
        Get valid access token (from cache or by authenticating)
        Returns: Valid JWT access token
        """
        with self._cache_lock:
            # Check if token exists and is still valid
            if self._cache_key in self._token_cache:
                cached_data = self._token_cache[self._cache_key]

                if self._is_token_valid(cached_data['token'], cached_data['expires_at']):
                    return cached_data['token']

            # Token doesn't exist or expired - get new one
            new_token = self._authenticate_and_cache()
            return new_token

    def get_or_fetch_token(self) -> str:
        """Alias for get_token to match user-provided patterns"""
        return self.get_token()
    
    def _authenticate_and_cache(self) -> str:
        """
        Authenticate and cache the new token.
        Tries USER_EMAIL first, then each user in USER_EMAIL_POOL if auth fails.
        Returns: New access token
        """
        pool_str = self.settings.USER_EMAIL_POOL
        candidates = [self.user_email]
        if pool_str:
            extras = [u.strip() for u in pool_str.split(",") if u.strip() and u.strip() != self.user_email]
            candidates.extend(extras)

        last_error = None
        for email in candidates:
            try:
                client = OAuth2Client(self.session, email, self.settings)
                access_token = client.authenticate()
                expires_at = self._get_token_expiration(access_token)
                self._token_cache[self._cache_key] = {
                    'token': access_token,
                    'expires_at': expires_at,
                    'cached_at': time.time()
                }
                if email != self.user_email:
                    logging.getLogger(__name__).warning(
                        "Primary user %s failed — authenticated as fallback user %s",
                        self.user_email, email,
                    )
                return access_token
            except Exception as e:
                last_error = e
                continue

        raise RuntimeError(f"All {len(candidates)} users failed to authenticate. Last error: {last_error}")
    
    @staticmethod
    def is_token_valid(token: str) -> bool:
        """
        Check if a JWT token is non-expired (with 60s buffer).
        Safe to call on any string — returns False on malformed input.
        """
        try:
            decoded = jwt.decode(token, options={"verify_signature": False})
            exp = decoded.get("exp", 0)
            return time.time() < (exp - 60)
        except Exception:
            return False

    @staticmethod
    def _is_token_valid(token: str, expires_at: float) -> bool:
        """
        Check if token is still valid
        Returns True if token will be valid for at least 60 more seconds
        """
        # Add 60 second buffer before expiration
        return time.time() < (expires_at - 60)
    
    @staticmethod
    def _get_token_expiration(token: str) -> float:
        """
        Decode JWT and get expiration timestamp
        Returns: Unix timestamp of expiration
        """
        try:
            # Decode without verification (we trust our auth server)
            decoded = jwt.decode(token, options={"verify_signature": False})
            exp = decoded.get('exp')
            
            if exp:
                return float(exp)
            
            # If no exp claim, assume 1 hour validity
            return time.time() + 3600
            
        except Exception:
            # If decode fails, assume 1 hour validity
            return time.time() + 3600
    
    def invalidate_token(self, user_email: Optional[str] = None):
        """
        Invalidate cached token(s)
        If user_email is None, invalidate current user's token
        """
        with self._cache_lock:
            key = self._cache_key if user_email is None else user_email
            if key in self._token_cache:
                del self._token_cache[key]
    
    @classmethod
    def clear_all_tokens(cls):
        """Clear all cached tokens (useful for test cleanup)"""
        with cls._cache_lock:
            cls._token_cache.clear()
    
    @classmethod
    def get_cache_info(cls) -> Dict:
        """
        Get information about cached tokens (for debugging)
        Returns: Dictionary with cache statistics
        """
        with cls._cache_lock:
            info = {
                'total_cached': len(cls._token_cache),
                'users': []
            }
            
            current_time = time.time()
            
            for email, data in cls._token_cache.items():
                time_left = data['expires_at'] - current_time
                info['users'].append({
                    'email': email,
                    'expires_in_seconds': max(0, int(time_left)),
                    'cached_at': datetime.fromtimestamp(data['cached_at']).isoformat(),
                    'is_valid': cls._is_token_valid(data['token'], data['expires_at'])
                })
            
            return info


class MultiUserTokenManager:
    """
    Manage tokens for multiple users
    Useful for tests that need to switch between users
    """
    
    def __init__(self, session: Session, settings: Settings):
        self.session = session
        self.settings = settings
        self._managers: Dict[str, TokenManager] = {}
    
    def get_token_for_user(self, user_email: str) -> str:
        """
        Get token for specific user
        Creates TokenManager for user if doesn't exist
        """
        if user_email not in self._managers:
            self._managers[user_email] = TokenManager(
                self.session, 
                user_email, 
                self.settings
            )
        
        return self._managers[user_email].get_token()
    
    def invalidate_user(self, user_email: str):
        """Invalidate specific user's token"""
        if user_email in self._managers:
            self._managers[user_email].invalidate_token()
    
    def clear_all(self):
        """Clear all user tokens"""
        TokenManager.clear_all_tokens()
        self._managers.clear()
