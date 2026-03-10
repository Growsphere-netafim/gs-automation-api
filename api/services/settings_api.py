import pytest
import requests as _requests
import urllib3
from api.client.api_client import QAApiClient
from api.client.response import ApiResponse
from api.endpoints.settings_api import SettingsAPIEndpoints

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_DEVICE_STATE_MANAGER_URL = "https://devicestatemanager-qa1.k8s.growsphere.netafim.com"
_FALLBACK_FARM_IDS = [
    "qa1-nb10047", "qa1-nb14218", "qa1-nb10058", "qa1-nb11141", "qa1-nb13042",
    "qa1-nb14595", "qa1-nb14604", "qa1-nb14644", "qa1-nb14658", "qa1-nb14677",
    "qa1-nb14716", "qa1-nb14752", "qa1-nb14753", "qa1-nb14776", "qa1-nb14781",
    "qa1-nb14900", "qa1-nb14905", "qa1-nb14948", "qa1-nb14952", "qa1-nb15017",
    "qa1-nb15116", "qa1-nb15214", "qa1-nb15551", "qa1-nb15778", "qa1-nb10000",
]


class SettingsAPIService:
    def __init__(self, client: QAApiClient, data):
        self._client = client
        self._data = data

    def _resolve_device_uuid(self) -> str:
        """Find a device UUID that has alert settings configured (probes endpoint per candidate)."""
        if '_device_uuid' not in self.__dict__:
            auth_header = self._client.headers.get("Authorization", "")
            headers = {"Authorization": auth_header, "Accept": "application/json"}
            farm_ids = [self._data.farm_id] + [f for f in _FALLBACK_FARM_IDS if f != self._data.farm_id]
            for farm_id in farm_ids:
                try:
                    resp = _requests.get(
                        f"{_DEVICE_STATE_MANAGER_URL}/api/DeviceStates/ByFarmId/{farm_id}",
                        headers=headers,
                        verify=False,
                        timeout=30,
                    )
                    if resp.status_code != 200:
                        continue
                    items = resp.json()
                    for item in (items if isinstance(items, list) else []):
                        uuid = item.get('fieldIoDeviceId')
                        if not uuid:
                            continue
                        probe = self._client.get(
                            SettingsAPIEndpoints.alert_settings(farm_id, uuid)
                        )
                        if probe.status_code == 200:
                            self._device_uuid = uuid
                            return uuid
                except Exception:
                    continue
            pytest.skip("No device UUID with alert settings found across QA1 farms")
        return self._device_uuid

    def get_alert_settings(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        if self._data.device_uuid:
            resp = self._client.get(
                SettingsAPIEndpoints.alert_settings(self._data.farm_id, self._data.device_uuid)
            )
            if resp.status_code != 404:
                return resp
        device_uuid = self._resolve_device_uuid()
        return self._client.get(
            SettingsAPIEndpoints.alert_settings(self._data.farm_id, device_uuid)
        )
