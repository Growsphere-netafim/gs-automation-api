import pytest
from api.client.api_client import QAApiClient
from api.client.response import ApiResponse
from api.endpoints.settings_api import SettingsAPIEndpoints


class SettingsAPIService:
    def __init__(self, client: QAApiClient, data):
        self._client = client
        self._data = data

    def get_alert_settings(self) -> ApiResponse:
        if not self._data.farm_id or not self._data.device_uuid:
            pytest.skip("farmId or deviceUuid not configured")
        return self._client.get(
            SettingsAPIEndpoints.alert_settings(self._data.farm_id, self._data.device_uuid)
        )
