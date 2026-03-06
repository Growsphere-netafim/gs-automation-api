import json
import logging
import pytest
import allure
import requests

logger = logging.getLogger(__name__)


class ApiResponse:
    def __init__(self, response: requests.Response):
        self._response = response

    @property
    def status_code(self) -> int:
        return self._response.status_code

    def json(self):
        return self._response.json()

    @property
    def text(self) -> str:
        return self._response.text

    def assert_ok(self):
        assert self._response.status_code == 200, (
            f"Expected 200, got {self._response.status_code}. "
            f"URL: {self._response.url}. Body: {self._response.text[:1000]}"
        )
        return self

    def assert_status(self, code: int):
        assert self._response.status_code == code, (
            f"Expected {code}, got {self._response.status_code}. "
            f"URL: {self._response.url}. Body: {self._response.text[:1000]}"
        )
        return self

    def assert_ok_or_skip_404(self, reason: str = "Resource not found (404)"):
        if self._response.status_code == 404:
            pytest.skip(reason)
        self.assert_ok()
        return self

    def assert_ok_or_skip(self, *skip_codes: int, reason: str = "Resource not available"):
        """Skip if status is in skip_codes, otherwise assert 200."""
        if self._response.status_code in skip_codes:
            pytest.skip(f"{reason} ({self._response.status_code})")
        self.assert_ok()
        return self

    def assert_any_of(self, *codes: int):
        assert self._response.status_code in codes, (
            f"Expected one of {codes}, got {self._response.status_code}. "
            f"URL: {self._response.url}. Body: {self._response.text[:1000]}"
        )
        return self

    def log_to_allure(self):
        try:
            req = self._response.request
            req_body = ""
            if req.body:
                try:
                    req_body = json.dumps(json.loads(req.body), indent=2)
                except Exception:
                    req_body = str(req.body)

            allure.attach(
                f"Method: {req.method}\nURL: {req.url}\nHeaders: {dict(req.headers)}\nBody: {req_body}",
                name="Request",
                attachment_type=allure.attachment_type.TEXT,
            )

            try:
                resp_body = json.dumps(self._response.json(), indent=2)
            except Exception:
                resp_body = self._response.text[:2000]

            allure.attach(
                f"Status: {self._response.status_code}\nBody: {resp_body}",
                name="Response",
                attachment_type=allure.attachment_type.TEXT,
            )
        except Exception as e:
            logger.warning(f"Failed to log to allure: {e}")
        return self
