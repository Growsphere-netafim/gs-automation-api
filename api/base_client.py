"""
Base API Client with common functionality
All specific API clients inherit from this
"""
from typing import Optional, Dict, Any, Union
from requests import Session, Response
import time
import logging

from core.token_manager import TokenManager
from config.settings import Settings, get_settings


logger = logging.getLogger(__name__)


class APIClient:
    """
    Base API client with authentication, retry logic, and common methods
    """
    
    def __init__(
        self, 
        session: Session, 
        user_email: str, 
        settings: Optional[Settings] = None
    ):
        self.session = session
        self.user_email = user_email
        self.settings = settings or get_settings()
        self.token_manager = TokenManager(session, user_email, self.settings)
        
        # Setup session defaults
        self.session.verify = False  # Skip SSL verification (adjust for production)
        self.base_url = ""           # To be set by subclasses
    
    def _build_url(self, endpoint: str) -> str:
        """
        Build full URL from base_url and endpoint
        """
        if endpoint.startswith(("http://", "https://")):
            return endpoint
        
        base = self.base_url.rstrip("/")
        path = endpoint.lstrip("/")
        return f"{base}/{path}"
        
    def _get_headers(self, additional_headers: Optional[Dict] = None) -> Dict:
        """
        Build request headers with authentication
        """
        access_token = self.token_manager.get_token()
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if additional_headers:
            headers.update(additional_headers)
        
        return headers
    
    def _make_request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        data: Optional[Any] = None,
        params: Optional[Dict] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
        **kwargs
    ) -> Response:
        """
        Make HTTP request with retry logic and error handling
        """
        timeout = timeout or self.settings.REQUEST_TIMEOUT
        max_retries = max_retries or self.settings.MAX_RETRIES
        
        # Get headers with auth token
        request_headers = self._get_headers(headers)
        
        attempt = 0
        last_exception = None
        
        while attempt < max_retries:
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    headers=request_headers,
                    json=json_data,
                    data=data,
                    params=params,
                    timeout=timeout,
                    **kwargs
                )
                
                # If token expired (401), invalidate and retry once
                if response.status_code == 401 and attempt == 0:
                    logger.warning("Token expired, refreshing...")
                    self.token_manager.invalidate_token()
                    request_headers = self._get_headers(headers)
                    attempt += 1
                    continue
                
                return response
                
            except Exception as e:
                last_exception = e
                attempt += 1
                
                if attempt < max_retries:
                    wait_time = self.settings.RETRY_DELAY * attempt
                    logger.warning(
                        f"Request failed (attempt {attempt}/{max_retries}): {e}. "
                        f"Retrying in {wait_time}s..."
                    )
                    time.sleep(wait_time)
                else:
                    logger.error(f"Request failed after {max_retries} attempts")
        
        # If we get here, all retries failed
        raise last_exception or Exception("Request failed")
    
    def get(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> Response:
        """Make GET request"""
        url = self._build_url(endpoint)
        return self._make_request("GET", url, params=params, headers=headers, **kwargs)
    
    def post(
        self,
        endpoint: str,
        json_data: Optional[Dict] = None,
        data: Optional[Any] = None,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> Response:
        """Make POST request"""
        url = self._build_url(endpoint)
        return self._make_request(
            "POST", url, json_data=json_data, data=data, headers=headers, **kwargs
        )
    
    def put(
        self,
        endpoint: str,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> Response:
        """Make PUT request"""
        url = self._build_url(endpoint)
        return self._make_request("PUT", url, json_data=json_data, headers=headers, **kwargs)
    
    def patch(
        self,
        endpoint: str,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> Response:
        """Make PATCH request"""
        url = self._build_url(endpoint)
        return self._make_request("PATCH", url, json_data=json_data, headers=headers, **kwargs)
    
    def delete(
        self,
        endpoint: str,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> Response:
        """Make DELETE request"""
        url = self._build_url(endpoint)
        return self._make_request("DELETE", url, headers=headers, **kwargs)
    
    def assert_status_code(
        self,
        response: Response,
        expected: Union[int, list],
        message: Optional[str] = None
    ):
        """
        Assert response status code
        """
        if isinstance(expected, int):
            expected = [expected]
        
        actual = response.status_code
        
        if actual not in expected:
            error_msg = message or (
                f"Expected status code {expected}, got {actual}. "
                f"Response: {response.text[:200]}"
            )
            raise AssertionError(error_msg)
    
    def assert_response_contains(
        self,
        response: Response,
        key: str,
        message: Optional[str] = None
    ):
        """
        Assert response JSON contains specific key
        """
        try:
            json_data = response.json()
        except Exception:
            raise AssertionError("Response is not valid JSON")
        
        if key not in json_data:
            error_msg = message or f"Response does not contain key '{key}'"
            raise AssertionError(error_msg)
    
    def assert_response_value(
        self,
        response: Response,
        key: str,
        expected_value: Any,
        message: Optional[str] = None
    ):
        """
        Assert response JSON key has expected value
        """
        try:
            json_data = response.json()
        except Exception:
            raise AssertionError("Response is not valid JSON")
        
        actual_value = json_data.get(key)
        
        if actual_value != expected_value:
            error_msg = message or (
                f"Expected {key}={expected_value}, got {actual_value}"
            )
            raise AssertionError(error_msg)
    
    def get_json(self, response: Response) -> Dict:
        """
        Safely get JSON from response
        """
        try:
            return response.json()
        except Exception as e:
            raise ValueError(f"Failed to parse JSON response: {e}")
    
    def is_success(self, response: Response) -> bool:
        """Check if response is successful (2xx status code)"""
        return 200 <= response.status_code < 300
    
    def log_request(self, method: str, url: str, **kwargs):
        """Log request details (useful for debugging)"""
        logger.info(f"{method} {url}")
        if kwargs.get('json_data'):
            logger.debug(f"Body: {kwargs['json_data']}")
    
    def log_response(self, response: Response):
        """Log response details (useful for debugging)"""
        logger.info(f"Response: {response.status_code}")
        try:
            logger.debug(f"Body: {response.json()}")
        except Exception:
            logger.debug(f"Body: {response.text[:200]}")
