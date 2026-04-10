"""
CORS preflight validation for the PROD Lookup Service (Azure instance).

The PROD user portal (https://produserportalst.z6.web.core.windows.net) makes requests
to the Azure-hosted lookup service (https://prod-netbeatvx-lookup-app-weu.azurewebsites.net).

When migration to k8s is complete, update _BASE_URL to the k8s URL.
"""
import allure
import pytest
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Azure-hosted PROD instance — currently active (k8s migration not yet complete)
_BASE_URL = "https://prod-netbeatvx-lookup-app-weu.azurewebsites.net"

# The PROD user portal origin that must be allowed
_ORIGIN = "https://produserportalst.z6.web.core.windows.net"

_CORS_ENDPOINTS = [
    "/api/Countries",  # public endpoint — no auth required
    # /api/Timezones requires Bearer auth — not suitable for unauthenticated CORS probing
]


@allure.epic("Lookup Service")
@allure.feature("CORS")
class TestLookupServiceCORS:

    @pytest.mark.parametrize("endpoint", _CORS_ENDPOINTS)
    @allure.story("OPTIONS preflight returns Access-Control-Allow-Origin")
    def test_cors_preflight(self, endpoint):
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
            f"OPTIONS preflight for {url} returned 405 — "
            f"CORS policy not configured for origin {_ORIGIN}."
        )
        assert "Access-Control-Allow-Origin" in response.headers, (
            f"CORS preflight failed for {url}: "
            f"'Access-Control-Allow-Origin' header is missing. "
            f"Status: {response.status_code}. "
            f"Headers: {dict(response.headers)}"
        )

    @pytest.mark.parametrize("endpoint", _CORS_ENDPOINTS)
    @allure.story("GET response includes Access-Control-Allow-Origin")
    def test_cors_get_response_header(self, endpoint):
        url = f"{_BASE_URL}{endpoint}"
        response = requests.get(
            url,
            headers={"Origin": _ORIGIN},
            verify=False,
            timeout=15,
        )
        assert response.status_code == 200, (
            f"GET {url} returned {response.status_code}. Body: {response.text[:500]}"
        )
        assert "Access-Control-Allow-Origin" in response.headers, (
            f"GET response for {url} is missing 'Access-Control-Allow-Origin'. "
            f"Headers: {dict(response.headers)}"
        )
