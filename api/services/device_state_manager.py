import pytest
from api.client.api_client import QAApiClient
from api.client.response import ApiResponse
from api.endpoints.device_state_manager import DeviceStateManagerEndpoints

_FALLBACK_FARM_IDS = [
    "qa1-nb10047", "qa1-nb14218", "qa1-nb10058", "qa1-nb11141", "qa1-nb13042",
    "qa1-nb14595", "qa1-nb14604", "qa1-nb14644", "qa1-nb14658", "qa1-nb14677",
    "qa1-nb14716", "qa1-nb14752", "qa1-nb14753", "qa1-nb14776", "qa1-nb14781",
    "qa1-nb14900", "qa1-nb14905", "qa1-nb14948", "qa1-nb14952", "qa1-nb15017",
    "qa1-nb15116", "qa1-nb15214", "qa1-nb15551", "qa1-nb15778", "qa1-nb10000",
]


class DeviceStateManagerService:
    def __init__(self, client: QAApiClient, data):
        self._client = client
        self._data = data

    def _resolve_device_uuid(self) -> str:
        if '_device_uuid' not in self.__dict__:
            farm_ids = [self._data.farm_id] + [f for f in _FALLBACK_FARM_IDS if f != self._data.farm_id]
            for farm_id in farm_ids:
                resp = self._client.get(DeviceStateManagerEndpoints.device_states_by_farm(farm_id))
                if resp.status_code != 200:
                    continue
                items = resp.json()
                for item in (items if isinstance(items, list) else []):
                    uuid = item.get('fieldIoDeviceId')
                    if uuid:
                        self._device_uuid = uuid
                        return uuid
            pytest.skip("No device UUID found across QA1 farms")
        return self._device_uuid

    def get_device_state_by_id(self) -> ApiResponse:
        if not self._data.device_id:
            pytest.skip("deviceId not configured")
        return self._client.get(
            DeviceStateManagerEndpoints.device_state_by_id(self._data.device_id)
        )

    def get_device_state_by_uuid(self) -> ApiResponse:
        device_uuid = self._data.device_uuid or self._resolve_device_uuid()
        return self._client.get(
            DeviceStateManagerEndpoints.device_state_by_uuid(device_uuid)
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
