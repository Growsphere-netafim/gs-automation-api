import pytest
import requests as _requests
import urllib3
from api.client.api_client import QAApiClient
from api.client.response import ApiResponse
from api.endpoints.irrigation import IrrigationEndpoints

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_FIELDIO_URL = "https://fieldio-qa1.k8s.growsphere.netafim.com"
_FALLBACK_FARM_IDS = [
    "qa1-nb10047", "qa1-nb14218", "qa1-nb10058", "qa1-nb11141", "qa1-nb13042",
    "qa1-nb14595", "qa1-nb14604", "qa1-nb14644", "qa1-nb14658", "qa1-nb14677",
    "qa1-nb14716", "qa1-nb14752", "qa1-nb14753", "qa1-nb14776", "qa1-nb14781",
    "qa1-nb14900", "qa1-nb14905", "qa1-nb14948", "qa1-nb14952", "qa1-nb15017",
    "qa1-nb15116", "qa1-nb15214", "qa1-nb15551", "qa1-nb15778", "qa1-nb10000",
]


class IrrigationService:
    def __init__(self, client: QAApiClient, data):
        self._client = client
        self._data = data

    def _resolve_io_id(self) -> str:
        """Query FieldIO to find a valid channelUuid across fallback farms."""
        if '_io_id' not in self.__dict__:
            auth_header = self._client.headers.get("Authorization", "")
            headers = {"Authorization": auth_header, "Accept": "application/json"}
            farm_ids = [self._data.farm_id] + [f for f in _FALLBACK_FARM_IDS if f != self._data.farm_id]
            for farm_id in farm_ids:
                try:
                    resp = _requests.get(
                        f"{_FIELDIO_URL}/api/io",
                        params={"farmId": farm_id},
                        headers=headers,
                        verify=False,
                        timeout=30,
                    )
                    if resp.status_code != 200:
                        continue
                    items = resp.json()
                    items = items if isinstance(items, list) else items.get('items', [])
                    for item in (items if isinstance(items, list) else []):
                        uuid = item.get('channelUuid') or item.get('id')
                        if uuid:
                            self._io_id = uuid
                            return uuid
                except Exception:
                    continue
            pytest.skip("No IO channel found across QA1 farms for irrigation")
        return self._io_id

    def get_io_modes(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        params = {
            "updatedDateUtc": self._data.updated_date_utc or None,
            "timestamp": self._data.timestamp or None,
        }
        return self._client.get(
            IrrigationEndpoints.io_modes(self._data.farm_id), params=params
        )

    def get_last_irrigation(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(IrrigationEndpoints.last_irrigation(self._data.farm_id))

    def get_last_eco_daily_program_scheme(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        params = {
            "daysBack": self._data.days_back or 7,
            "deviceUUid": self._data.device_uuid or None,
            "deviceProgramId": self._data.device_program_id or None,
        }
        return self._client.get(
            IrrigationEndpoints.last_eco_daily_program_scheme(self._data.farm_id),
            params=params,
        )

    def get_daily_irrigation(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        io_id = self._data.io_id or self._resolve_io_id()
        params = {
            "ioId": io_id,
            "fromDate": self._data.start_date or None,
            "toDate": self._data.end_date or None,
        }
        return self._client.get(
            IrrigationEndpoints.daily_irrigation(self._data.farm_id), params=params
        )

    def get_daily_eco_flex_report(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        params = {
            "deviceId": self._data.device_uuid or None,
            "date": self._data.date or None,
        }
        return self._client.get(
            IrrigationEndpoints.daily_eco_flex_report(self._data.farm_id), params=params
        )

    def get_eco_flex_controller_report(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        params = {
            "fromDate": self._data.start_date or None,
            "toDate": self._data.end_date or None,
        }
        return self._client.get(
            IrrigationEndpoints.eco_flex_controller_report(self._data.farm_id), params=params
        )

    def get_mainline(self) -> ApiResponse:
        if not self._data.farm_id or not self._data.device_uuid or not self._data.mainline_id:
            pytest.skip("farmId, deviceUuid or mainlineId not configured")
        return self._client.get(
            IrrigationEndpoints.mainline(
                self._data.farm_id, self._data.device_uuid, self._data.mainline_id
            )
        )

    def get_device_mainlines(self) -> ApiResponse:
        if not self._data.farm_id or not self._data.device_uuid:
            pytest.skip("farmId or deviceUuid not configured")
        return self._client.get(
            IrrigationEndpoints.device_mainlines(self._data.farm_id, self._data.device_uuid)
        )

    def get_odata_alarms(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(
            IrrigationEndpoints.odata_alarms(self._data.farm_id), params={"$top": 10}
        )

    def get_odata_irrigation_logs(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(
            IrrigationEndpoints.odata_irrigation_logs(self._data.farm_id), params={"$top": 10}
        )

    def get_program_schemes(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(IrrigationEndpoints.program_schemes(self._data.farm_id))

    def get_program_scheme(self) -> ApiResponse:
        if not self._data.program_uuid:
            pytest.skip("programUuid not configured")
        return self._client.get(
            IrrigationEndpoints.program_scheme(self._data.program_uuid),
            params={"bringEmptyProgram": True},
        )

    def get_irrigation_programs_status(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(
            IrrigationEndpoints.irrigation_programs_status(self._data.farm_id)
        )

    def get_recipes(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(IrrigationEndpoints.recipes(self._data.farm_id))
