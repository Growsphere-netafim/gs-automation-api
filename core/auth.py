"""
OAuth2 + PKCE Authentication Handler
Based on your existing auth.py with improvements
"""
import logging
import string
import base64
import hashlib
from secrets import choice, token_urlsafe
from urllib.parse import parse_qs, urlparse, urljoin
from typing import Optional, Dict, Any
from bs4 import BeautifulSoup
import requests
from requests import Session

from config.settings import Settings

logger = logging.getLogger(__name__)

_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def _mask(value: str, show: int = 4) -> str:
    """Show first N chars only — safe for logs."""
    if not value:
        return "<empty>"
    return value[:show] + "***"


class OAuth2Client:
    """
    Handles OAuth2 authentication with PKCE flow
    Supports your existing Auth0 + Identity Server flow
    """

    def __init__(self, session: Session, user_email: str, settings: Settings):
        self.user_email = user_email
        self.user_password = settings.PASSWORD
        ids_base = settings.IDS_URL.rstrip("/")
        self.auth_url = f"{ids_base}/connect/authorize"
        self.token_url = f"{ids_base}/connect/token"
        self.oidc_client_id = settings.OIDC_CLIENT_ID
        self.oidc_redirect_uri = settings.OIDC_REDIRECT_URI
        self.scopes = settings.SCOPES_VAL
        self.session = session
        self.env_name = settings.ENV_NAME

        # PKCE parameters
        self.state = self._generate_random_string()
        self.code_verifier = self._generate_code_verifier()
        self.code_challenge = self._generate_code_challenge(self.code_verifier)

        # Build authorization URL
        self.authorization_url = self._build_authorization_url()

    @staticmethod
    def _generate_random_string(size: int = 16) -> str:
        """Generate random string for state parameter"""
        alphabet = string.ascii_letters + string.digits
        return "".join([choice(alphabet) for _ in range(size)])

    @staticmethod
    def _generate_code_verifier(length: int = 128) -> str:
        """
        Generate PKCE code verifier
        Must be 43-128 characters long
        """
        length = max(43, min(length, 128))
        return token_urlsafe(length)[:length]

    @staticmethod
    def _generate_code_challenge(code_verifier: str) -> str:
        """
        Generate PKCE code challenge from verifier
        SHA256 hash + base64url encoding
        """
        sha256_hash = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(sha256_hash).decode('utf-8').rstrip('=')
        return code_challenge

    def _build_authorization_url(self) -> str:
        """Build OAuth2 authorization URL with PKCE parameters"""
        params = {
            "client_id": self.oidc_client_id,
            "redirect_uri": self.oidc_redirect_uri,
            "response_type": "code",
            "scope": self.scopes,
            "state": self.state,
            "code_challenge": self.code_challenge,
            "code_challenge_method": "S256",
            "response_mode": "query"
        }

        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.auth_url}?{query_string}"

    def _get_csrf_token(self) -> tuple[str, str, str]:
        """
        Make initial authorization request to get CSRF token
        Returns: (csrf_token, base_uri, query_string)
        """
        response = self.session.get(
            self.authorization_url,
            headers=_BROWSER_HEADERS,
            timeout=45,
            allow_redirects=True
        )

        csrf_token = self.session.cookies.get('_csrf')
        if not csrf_token:
            logger.error(
                "No _csrf cookie in auth response. Status: %s. Body: %s",
                response.status_code,
                response.text[:500],
            )
            raise ValueError("Failed to get CSRF token from authorization endpoint")

        parsed_url = urlparse(response.url)
        base_uri = f"{parsed_url.scheme}://{parsed_url.netloc}"
        query_string = parsed_url.query

        return csrf_token, base_uri, query_string

    def _perform_login(self, csrf_token: str, base_uri: str, query_string: str) -> requests.Response:
        """
        Submit login credentials to Auth0
        Returns: Login response
        """
        query_params = parse_qs(query_string)

        # Determine tenant based on environment
        tenant = "netafim-qa" if self.env_name != "prod" else "netafim"

        login_payload = {
            "client_id": query_params.get('client', [None])[0],
            "redirect_uri": query_params.get('redirect_uri', [None])[0],
            "tenant": tenant,
            "response_type": query_params.get('response_type', [None])[0],
            "scope": "openid profile email",
            "_csrf": csrf_token,
            "state": query_params.get('state', [None])[0],
            "_intstate": "deprecated",
            "nonce": query_params.get('nonce', [None])[0],
            "password": self.user_password,
            "connection": "Username-Password-Authentication",
            "username": self.user_email
        }

        login_url = f"{base_uri}/usernamepassword/login"

        response = self.session.post(
            login_url,
            json=login_payload,
            headers={**_BROWSER_HEADERS, 'Content-Type': 'application/json'},
            verify=False,
            timeout=40
        )

        if response.status_code != 200:
            logger.warning(
                "Auth0 login returned %s. Body: %s",
                response.status_code,
                response.text[:500],
            )

        return response

    def _follow_redirects(self, login_response: requests.Response) -> Optional[str]:
        """
        Follow OAuth redirect chain until final redirect URI
        Returns: Final redirect URI with authorization code
        """
        html_content = login_response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        form = soup.find('form', {'name': 'hiddenform'})

        if not form:
            logger.error(
                "No hidden form found in Auth0 login response. "
                "Status: %s. Body preview: %s",
                login_response.status_code,
                html_content[:1000],
            )
            raise ValueError("No hidden form found in login response")

        action_url = form['action']
        form_data = {
            input_tag['name']: input_tag['value']
            for input_tag in form.find_all('input', {'type': 'hidden'})
        }

        current_response = self.session.post(action_url, data=form_data, allow_redirects=False)

        # Follow redirect chain
        while 300 <= current_response.status_code < 400 or 'form' in current_response.text.lower():
            if 'form' in current_response.text.lower():
                soup = BeautifulSoup(current_response.text, 'html.parser')
                form = soup.find('form')
                action_url = form['action']
                form_data = {
                    input_tag['name']: input_tag['value']
                    for input_tag in form.find_all('input', {'type': 'hidden'})
                }
                current_response = self.session.post(
                    action_url,
                    data=form_data,
                    allow_redirects=False,
                    verify=False
                )
            else:
                redirect_url = current_response.headers.get('Location')
                if not redirect_url:
                    break

                redirect_url = urljoin(current_response.url, redirect_url)

                # Check if we reached the final redirect URI
                if redirect_url.startswith(self.oidc_redirect_uri):
                    return redirect_url

                current_response = self.session.get(redirect_url, allow_redirects=False)

        logger.error(
            "Redirect chain ended without reaching redirect URI. Last status: %s",
            current_response.status_code,
        )
        return None

    def _exchange_code_for_token(self, redirect_uri: str) -> str:
        """
        Exchange authorization code for access token
        Returns: Access token (JWT)
        """
        parsed_url = urlparse(redirect_uri)
        query_params = parse_qs(parsed_url.query)

        auth_code = query_params.get("code")
        if not auth_code:
            raise ValueError("No authorization code found in redirect URI")

        token_payload = {
            "client_id": self.oidc_client_id,
            "code": auth_code[0],
            "redirect_uri": self.oidc_redirect_uri,
            "code_verifier": self.code_verifier,
            "grant_type": "authorization_code"
        }

        response = self.session.post(
            self.token_url,
            data=token_payload,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            verify=False,
            timeout=30
        )

        if response.status_code != 200:
            raise ValueError(f"Token exchange failed: {response.status_code} - {response.text}")

        token_data = response.json()
        access_token = token_data.get('access_token')

        if not access_token:
            raise ValueError("No access token in response")

        return access_token

    def _try_ropc(self) -> Optional[str]:
        """
        Try ROPC (Resource Owner Password Credentials) grant.
        Sends username+password directly to IDS — no HTML scraping, works from any IP.
        Returns: Access token or None if not supported.
        """
        payload = {
            "grant_type": "password",
            "client_id": self.oidc_client_id,
            "username": self.user_email,
            "password": self.user_password,
            "scope": self.scopes.replace("%20", " "),
        }
        try:
            response = self.session.post(
                self.token_url,
                data=payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                verify=False,
                timeout=30,
            )
            if response.status_code == 200:
                return response.json().get("access_token")
            logger.debug("ROPC not supported (status %s) — falling back to PKCE", response.status_code)
        except Exception as e:
            logger.debug("ROPC exception: %s — falling back to PKCE", e)

        return None

    def _authenticate_pkce(self) -> str:
        """
        Execute complete OAuth2 + PKCE authentication flow (browser simulation).
        Returns: JWT access token
        """
        # Clear any existing cookies
        self.session.cookies.clear()

        # Step 1: Get CSRF token
        csrf_token, base_uri, query_string = self._get_csrf_token()

        # Step 2: Submit login credentials
        login_response = self._perform_login(csrf_token, base_uri, query_string)

        # Step 3: Follow redirects to get authorization code
        final_redirect_uri = self._follow_redirects(login_response)

        if not final_redirect_uri:
            raise ValueError("Failed to get final redirect URI with authorization code")

        # Step 4: Exchange code for access token
        return self._exchange_code_for_token(final_redirect_uri)

    def authenticate(self) -> str:
        """
        Authenticate and return a JWT access token.
        Tries ROPC first (works from any IP including CI).
        Falls back to PKCE + Auth0 browser flow if ROPC is not supported.
        """
        token = self._try_ropc()
        if token:
            return token

        return self._authenticate_pkce()


class TokenRefresher:
    """
    Handle token refresh if your API supports refresh tokens
    """

    def __init__(self, session: Session, settings: Settings):
        self.session = session
        self.token_url = f"{settings.IDS_URL}/connect/token"
        self.client_id = settings.OIDC_CLIENT_ID

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh access token using refresh token
        Returns: New token data
        """
        payload = {
            "client_id": self.client_id,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }

        response = self.session.post(
            self.token_url,
            data=payload,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        if response.status_code != 200:
            raise ValueError(f"Token refresh failed: {response.status_code}")

        return response.json()
