import logging
import urllib3
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from api.client.response import ApiResponse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)

_TIMEOUT = 45
_RETRIES = 3
_RETRY_STATUSES = (500, 502, 503, 504)


class QAApiClient:
    def __init__(self, base_url: str, token: str = None, headers: dict = None):
        self.base_url = base_url.rstrip("/")
        self._session = requests.Session()
        self._session.verify = False

        retry = Retry(
            total=_RETRIES,
            backoff_factor=1,
            status_forcelist=_RETRY_STATUSES,
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry)
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
        if headers:
            self.headers.update(headers)

    def get(
        self,
        endpoint: str,
        params: dict = None,
        headers: dict = None,
        json: dict = None,
        expected_status: int = None,
    ) -> ApiResponse:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        req_headers = self.headers.copy()
        if headers:
            req_headers.update(headers)

        logger.info(f"GET {url}")
        if params:
            logger.info(f"Params: {params}")

        response = self._session.get(
            url, headers=req_headers, params=params, json=json, timeout=_TIMEOUT
        )
        logger.info(f"Status: {response.status_code}")

        api_response = ApiResponse(response)
        if expected_status is not None:
            api_response.assert_status(expected_status)

        return api_response

    def post(
        self,
        endpoint: str,
        json: dict = None,
        params: dict = None,
        headers: dict = None,
    ) -> ApiResponse:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        req_headers = self.headers.copy()
        if headers:
            req_headers.update(headers)

        logger.info(f"POST {url}")
        response = self._session.post(
            url, headers=req_headers, json=json, params=params, timeout=_TIMEOUT
        )
        logger.info(f"Status: {response.status_code}")
        return ApiResponse(response)
