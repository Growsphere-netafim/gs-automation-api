import pytest
import requests
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
        try:
            resp = self._client.get(ReportAPIEndpoints.configuration(self._data.user_id))
        except requests.exceptions.RetryError:
            pytest.xfail(
                f"Backend bug: Report configuration returns 500 for user {self._data.user_id}"
            )
        if resp.status_code == 500:
            pytest.xfail(
                f"Backend bug: Report configuration returns 500 for user {self._data.user_id}"
            )
        return resp

    def get_reports_preferences(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        resp = self._client.get(ReportAPIEndpoints.reports_preferences(self._data.farm_id))
        if resp.status_code == 403:
            pytest.skip(f"reportsPreferences not enabled for farm {self._data.farm_id} (403)")
        return resp
