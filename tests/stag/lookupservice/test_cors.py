"""
CORS preflight validation for the Stag Lookup Service.

Context: A CORS bug was reported where browser requests from the staging user-portal
(https://staguserportalst.z6.web.core.windows.net) to the Lookup Service were blocked
because the server did not return 'Access-Control-Allow-Origin' on preflight responses.

These tests simulate the browser's OPTIONS preflight and GET requests directly at the HTTP
level using requests (no browser required). They will FAIL if CORS headers are missing,
catching the bug class before it reaches frontend users.
"""
import allure
import pytest
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# The k8s-hosted stag instance used by the frontend (confirmed by CORS bug report)
_BASE_URL = "https://lookup-stag.k8s.growsphere.netafim.com"

# The frontend origin that must be allowed
_ORIGIN = "https://staguserportalst.z6.web.core.windows.net"

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
        return 'Access-Control-Allow-Origin' — which is the exact failure mode
        observed in the CORS bug report."""
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
        """Verifies that actual GET responses also carry the CORS header when
        an Origin is sent. Some servers only set it on preflight, not on the
        actual request — both must be present for the browser to allow the XHR."""
        url = f"{_BASE_URL}{endpoint}"
        response = requests.get(
            url,
            headers={"Origin": _ORIGIN},
            verify=False,
            timeout=15,
        )
        assert response.status_code == 200, (
            f"GET {url} returned {response.status_code}. "
            f"Body: {response.text[:500]}"
        )
        assert "Access-Control-Allow-Origin" in response.headers, (
            f"GET response for {url} is missing 'Access-Control-Allow-Origin'. "
            f"Response headers: {dict(response.headers)}"
        )
