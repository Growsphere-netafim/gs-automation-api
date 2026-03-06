import pytest
from api.client.api_client import QAApiClient
from api.client.response import ApiResponse
from api.endpoints.device_state_manager import DeviceStateManagerEndpoints


class DeviceStateManagerService:
    def __init__(self, client: QAApiClient, data):
        self._client = client
        self._data = data

    def get_device_state_by_id(self) -> ApiResponse:
        if not self._data.device_id:
            pytest.skip("deviceId not configured")
        return self._client.get(
            DeviceStateManagerEndpoints.device_state_by_id(self._data.device_id)
        )

    def get_device_state_by_uuid(self) -> ApiResponse:
        if not self._data.device_uuid:
            pytest.skip("deviceUuid not configured")
        return self._client.get(
            DeviceStateManagerEndpoints.device_state_by_uuid(self._data.device_uuid)
        )

    def get_device_states_by_farm(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(
            DeviceStateManagerEndpoints.device_states_by_farm(self._data.farm_id)
        )

    def get_heartbeats(self) -> ApiResponse:
        if not self._data.from_date_time_utc or not self._data.to_date_time_utc:
            pytest.skip("Date range parameters not configured")
        params = {
            "fromDateTimeUtc": self._data.from_date_time_utc,
            "toDateTimeUtc": self._data.to_date_time_utc,
            "systemType": self._data.system_type,
            "deviceId": self._data.device_id,
            "page": 1,
            "pageSize": 10,
        }
        return self._client.get(DeviceStateManagerEndpoints.heartbeats(), params=params)

    def query_heartbeats(self) -> ApiResponse:
        if not self._data.from_date_time_utc or not self._data.to_date_time_utc:
            pytest.skip("Date range parameters not configured")
        params = {
            "fromDateTimeUtc": self._data.from_date_time_utc,
            "toDateTimeUtc": self._data.to_date_time_utc,
            "systemType": self._data.system_type,
            "page": 1,
            "pageSize": 10,
        }
        if self._data.device_id:
            params["deviceIds"] = [self._data.device_id]
        return self._client.get(DeviceStateManagerEndpoints.query_heartbeats(), params=params)
