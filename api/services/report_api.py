import pytest
from api.client.api_client import QAApiClient
from api.client.response import ApiResponse
from api.endpoints.report_api import ReportAPIEndpoints


class ReportAPIService:
    def __init__(self, client: QAApiClient, data):
        self._client = client
        self._data = data

    def get_configuration(self) -> ApiResponse:
        if not self._data.user_id:
            pytest.skip("userId not configured")
        return self._client.get(ReportAPIEndpoints.configuration(self._data.user_id))

    def get_reports_preferences(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        resp = self._client.get(ReportAPIEndpoints.reports_preferences(self._data.farm_id))
        if resp.status_code == 403:
            pytest.skip(f"Reports preferences for farm {self._data.farm_id} returned 403 (no access)")
        return resp
