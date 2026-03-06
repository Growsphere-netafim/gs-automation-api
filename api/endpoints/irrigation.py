from typing import List, Dict, Any
from requests import Response


class IrrigationAPI:
    """Legacy API client for Irrigation — kept for backward compatibility with integration tests."""

    def __init__(self, session, user_email: str):
        from api.base_client import APIClient
        from config.settings import get_settings
        # Lazy import to avoid circular dependency issues
        self._session = session
        self._user_email = user_email
        settings = get_settings()
        self.base_url = f"{settings.base_urls.get('irrigation_url', 'https://irrigation-qa1.k8s.growsphere.netafim.com')}/api/v1"

    def _get(self, path: str, **kwargs) -> Response:
        url = f"{self.base_url}{path}"
        return self._session.get(url, **kwargs)

    def _post(self, path: str, json_data=None, **kwargs) -> Response:
        url = f"{self.base_url}{path}"
        return self._session.post(url, json=json_data, **kwargs)

    def dismiss_farm_alarms(self, farm_id: str, alarm_ids: List[str]) -> Response:
        return self._post(f"/farms/{farm_id}/dismiss-alarms", json_data=alarm_ids)

    def dismiss_device_alarms(self, farm_id: str, device_id: str, alarm_ids: List[str]) -> Response:
        return self._post(f"/farms/{farm_id}/devices/{device_id}/dismiss-alarms", json_data=alarm_ids)

    def get_irrigation_status(self, farm_id: str) -> Response:
        return self._get(f"/farms/{farm_id}/irrigation-status")

    def start_irrigation(self, farm_id: str, irrigation_data: Dict[str, Any]) -> Response:
        return self._post(f"/farms/{farm_id}/irrigation/start", json_data=irrigation_data)

    def stop_irrigation(self, farm_id: str, program_id: str) -> Response:
        return self._post(f"/farms/{farm_id}/irrigation/stop/{program_id}")


class IrrigationEndpoints:
    @staticmethod
    def io_modes(farm_id: str) -> str:
        return f"api/v1/farms/{farm_id}/io-modes"

    @staticmethod
    def last_irrigation(farm_id: str) -> str:
        return f"api/v1/farms/{farm_id}/LastIrrigation"

    @staticmethod
    def last_eco_daily_program_scheme(farm_id: str) -> str:
        return f"api/v1/farms/{farm_id}/LastEcoDailyProgramScheme"

    @staticmethod
    def daily_irrigation(farm_id: str) -> str:
        return f"api/v1/farms/{farm_id}/DailyIrrigation"

    @staticmethod
    def daily_eco_flex_report(farm_id: str) -> str:
        return f"api/v1/farms/{farm_id}/DailyEcoFlexReport"

    @staticmethod
    def eco_flex_controller_report(farm_id: str) -> str:
        return f"api/v1/farms/{farm_id}/GetEcoFlexControllerReport"

    @staticmethod
    def mainline(farm_id: str, device_uuid: str, mainline_id) -> str:
        return f"api/v1/farms/{farm_id}/devices/{device_uuid}/mainlines/{mainline_id}"

    @staticmethod
    def device_mainlines(farm_id: str, device_uuid: str) -> str:
        return f"api/v1/farms/{farm_id}/devices/{device_uuid}/mainlines"

    @staticmethod
    def odata_alarms(farm_id: str) -> str:
        return f"api/v1/farms/{farm_id}/odata/alarms"

    @staticmethod
    def odata_irrigation_logs(farm_id: str) -> str:
        return f"api/v1/farms/{farm_id}/odata/irrigation-logs"

    @staticmethod
    def program_schemes(farm_id: str) -> str:
        return f"api/v1/farms/{farm_id}/programSchemes"

    @staticmethod
    def program_scheme(program_uuid: str) -> str:
        return f"api/v1/programSchemes/{program_uuid}"

    @staticmethod
    def irrigation_programs_status(farm_id: str) -> str:
        return f"api/v1/farms/{farm_id}/irrigation-programs-status"

    @staticmethod
    def recipes(farm_id: str) -> str:
        return f"api/v1/farms/{farm_id}/recipes"
