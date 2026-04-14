"""
CORS preflight validation for the QA1 Lookup Service (k8s instance).

The QA1 user portal (https://qa1userportalst.z6.web.core.windows.net) makes requests
to the k8s-hosted lookup service (https://lookup-qa1.k8s.growsphere.netafim.com).

Current status: OPTIONS preflight returns 405 Method Not Allowed and is missing
Access-Control-Allow-Origin — this is an active bug that blocks the portal.

These tests will FAIL until the k8s ingress is configured with the correct CORS policy.
"""
import allure
import pytest
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# k8s-hosted QA1 instance — used by the QA1 user portal
_BASE_URL = "https://lookup-qa1.k8s.growsphere.netafim.com"

# The frontend origin that must be allowed
_ORIGIN = "https://qa1userportalst.z6.web.core.windows.net"

_CORS_ENDPOINTS = [
    "/api/Countries",
    "/api/Timezones",
]


@allure.epic("Lookup Service")
@allure.feature("CORS")
class TestLookupServiceCORS:

    @pytest.mark.parametrize("endpoint", _CORS_ENDPOINTS)
    @allure.story("OPTIONS preflight returns Access-Control-Allow-Origin")
    def test_cors_preflight(self, endpoint):
        """Simulates the browser OPTIONS preflight. Fails if the server does not
        return 'Access-Control-Allow-Origin' or returns 405 — the current failure
        mode on the QA1 k8s ingress."""
        url = f"{_BASE_URL}{endpoint}"
        response = requests.options(
            url,
            headers={
                "Origin": _ORIGIN,
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "Authorization,Content-Type",
            },
            verify=False,
            timeout=15,
        )
        assert response.status_code != 405, (
            f"OPTIONS preflight for {url} returned 405 Method Not Allowed — "
            f"the k8s ingress is not handling OPTIONS requests. "
            f"CORS policy must be configured to allow origin {_ORIGIN}."
        )
        assert "Access-Control-Allow-Origin" in response.headers, (
            f"CORS preflight failed for {url}: "
            f"'Access-Control-Allow-Origin' header is missing. "
            f"Status: {response.status_code}. "
            f"Response headers: {dict(response.headers)}"
        )
        allowed_origin = response.headers["Access-Control-Allow-Origin"]
        assert allowed_origin in (_ORIGIN, "*"), (
            f"Origin '{_ORIGIN}' is not allowed. "
            f"'Access-Control-Allow-Origin' was: '{allowed_origin}'"
        )

    @pytest.mark.parametrize("endpoint", _CORS_ENDPOINTS)
    @allure.story("GET response includes Access-Control-Allow-Origin")
    def test_cors_get_response_header(self, endpoint):
        """Verifies that actual GET responses carry the CORS header when
        an Origin is sent.

        Note: some endpoints require authentication and return 401 when called
        without a token. A 401 with Access-Control-Allow-Origin present is a
        correct CORS response — the browser can read the error and handle auth.
        We accept 200 or 401 as valid; both confirm CORS is active.
        Server errors (5xx) or missing CORS headers are the true failure modes.
        """
        url = f"{_BASE_URL}{endpoint}"
        response = requests.get(
            url,
            headers={"Origin": _ORIGIN},
            verify=False,
            timeout=15,
        )
        assert response.status_code < 500, (
            f"GET {url} returned unexpected server error {response.status_code}. "
            f"Body: {response.text[:500]}"
        )
        assert "Access-Control-Allow-Origin" in response.headers, (
            f"GET response for {url} is missing 'Access-Control-Allow-Origin'. "
            f"Status: {response.status_code}. "
            f"Response headers: {dict(response.headers)}"
        )
        allowed_origin = response.headers["Access-Control-Allow-Origin"]
        assert allowed_origin in (_ORIGIN, "*"), (
            f"Origin '{_ORIGIN}' is not allowed by GET response for {url}. "
            f"'Access-Control-Allow-Origin' was: '{allowed_origin}'"
        )
