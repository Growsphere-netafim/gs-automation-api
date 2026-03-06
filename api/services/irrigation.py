import pytest
from api.client.api_client import QAApiClient
from api.client.response import ApiResponse
from api.endpoints.irrigation import IrrigationEndpoints


class IrrigationService:
    def __init__(self, client: QAApiClient, data):
        self._client = client
        self._data = data

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
        params = {
            "ioId": self._data.io_id or None,
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
