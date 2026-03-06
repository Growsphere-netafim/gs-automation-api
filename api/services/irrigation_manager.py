import pytest
from api.client.api_client import QAApiClient
from api.client.response import ApiResponse
from api.endpoints.irrigation_manager import IrrigationManagerEndpoints


class IrrigationManagerService:
    def __init__(self, client: QAApiClient, data):
        self._client = client
        self._data = data

    def get_active_commands(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(
            IrrigationManagerEndpoints.active_commands(self._data.farm_id),
            headers={"farmId": self._data.farm_id}
        )
