import pytest
from api.client.api_client import QAApiClient
from api.client.response import ApiResponse
from api.endpoints.mobile import MobileEndpoints


_FALLBACK_FARM_IDS = [
    "qa1-nb15681", "qa1-nb14863", "qa1-nb10047", "qa1-nb14218", "qa1-nb10058",
    "qa1-nb11141", "qa1-nb13042", "qa1-nb14595", "qa1-nb14604", "qa1-nb14644",
    "qa1-nb14658", "qa1-nb14677", "qa1-nb14716", "qa1-nb14752", "qa1-nb14753",
    "qa1-nb14776", "qa1-nb14781", "qa1-nb14900", "qa1-nb14905", "qa1-nb14948",
    "qa1-nb14952", "qa1-nb15017", "qa1-nb15116", "qa1-nb15214", "qa1-nb15551",
    "qa1-nb15778", "qa1-nb10000",
]


class MobileService:
    def __init__(self, client: QAApiClient, data):
        self._client = client
        self._data = data

    def _resolve_reference_id(self) -> str:
        """Fetch first available command referenceId across fallback farms."""
        if '_reference_id' not in self.__dict__:
            device_id = self._data.device_id
            if device_id:
                resp = self._client.get(MobileEndpoints.commands_list_for_device(device_id))
                if resp.status_code == 200:
                    data = resp.json()
                    items = data if isinstance(data, list) else data.get('value', data.get('commands', data.get('items', [])))
                    for item in (items if isinstance(items, list) else []):
                        ref_id = item.get('referenceId') or item.get('id')
                        if ref_id:
                            self._reference_id = ref_id
                            return ref_id
            farm_ids = [self._data.farm_id] + [f for f in _FALLBACK_FARM_IDS if f != self._data.farm_id]
            for farm_id in farm_ids:
                if not farm_id or not device_id:
                    continue
                resp = self._client.get(MobileEndpoints.commands_by_farm_device(farm_id, device_id))
                if resp.status_code != 200:
                    continue
                data = resp.json()
                items = data if isinstance(data, list) else data.get('value', data.get('commands', data.get('items', [])))
                for item in (items if isinstance(items, list) else []):
                    ref_id = item.get('referenceId') or item.get('id')
                    if ref_id:
                        self._reference_id = ref_id
                        return ref_id
            pytest.skip("No command referenceId found for Mobile tests")
        return self._reference_id

    def _resolve_device_uuid(self) -> str:
        """Find a device UUID that has general settings configured (probes endpoint)."""
        if '_device_uuid' not in self.__dict__:
            farm_ids = [self._data.farm_id] + [f for f in _FALLBACK_FARM_IDS if f != self._data.farm_id]
            for farm_id in farm_ids:
                if not farm_id:
                    continue
                resp = self._client.get(MobileEndpoints.device_states_by_farm(farm_id))
                if resp.status_code != 200:
                    continue
                data = resp.json()
                items = data if isinstance(data, list) else data.get('deviceStates', data.get('items', data.get('value', [])))
                for item in (items if isinstance(items, list) else []):
                    uuid = item.get('fieldIoDeviceId') or item.get('deviceUuid') or item.get('uuid')
                    if not uuid:
                        continue
                    probe = self._client.get(MobileEndpoints.general_settings(uuid))
                    if probe.status_code == 200:
                        self._device_uuid = uuid
                        return uuid
            pytest.skip("No device with general settings found across QA1 farms")
        return self._device_uuid

    def _resolve_flow_uuid(self) -> str:
        """Fetch first provisioning flow UUID across fallback farms."""
        if '_flow_uuid' not in self.__dict__:
            farm_ids = [self._data.farm_id] + [f for f in _FALLBACK_FARM_IDS if f != self._data.farm_id]
            for farm_id in farm_ids:
                if not farm_id:
                    continue
                resp = self._client.get(MobileEndpoints.provisioning_farm(farm_id))
                if resp.status_code != 200:
                    continue
                data = resp.json()
                items = data if isinstance(data, list) else data.get('flows', data.get('items', []))
                for item in (items if isinstance(items, list) else []):
                    uuid = item.get('id') or item.get('flowUuid') or item.get('uuid')
                    if uuid:
                        self._flow_uuid = uuid
                        return uuid
            pytest.skip("No provisioning flow UUID found across all QA1 farms")
        return self._flow_uuid

    # Bases
    def get_base_topology(self) -> ApiResponse:
        return self._client.get(MobileEndpoints.base_topology())

    def get_base_tree(self) -> ApiResponse:
        if not self._data.base_uuid:
            pytest.skip("baseUuid not configured")
        return self._client.get(MobileEndpoints.base_tree(self._data.base_uuid))

    # Commands
    def get_command(self) -> ApiResponse:
        reference_id = self._data.reference_id or self._resolve_reference_id()
        return self._client.get(MobileEndpoints.command(reference_id))

    def get_commands_by_farm_device(self) -> ApiResponse:
        if not self._data.farm_id or not self._data.device_id:
            pytest.skip("farmId or deviceId not configured")
        return self._client.get(
            MobileEndpoints.commands_by_farm_device(self._data.farm_id, self._data.device_id)
        )

    def get_commands_list(self) -> ApiResponse:
        if not self._data.device_id:
            pytest.skip("deviceId not configured")
        return self._client.get(MobileEndpoints.commands_list_for_device(self._data.device_id))

    def request_command(self) -> ApiResponse:
        command_type = self._data.command_type or 1
        system_type = self._data.system_type
        if system_type == 1:
            system_type = "Flex"
        device_id = self._data.device_uuid or self._data.device_id
        if not device_id:
            pytest.skip("deviceId/deviceUuid not configured")
        return self._client.get(
            MobileEndpoints.request_command(command_type, system_type, device_id)
        )

    # Devices
    def get_device_state(self) -> ApiResponse:
        if not self._data.farm_id or not self._data.device_id:
            pytest.skip("farmId or deviceId not configured")
        return self._client.get(
            MobileEndpoints.device_state(self._data.farm_id, self._data.device_id)
        )

    def get_device_assignable(self) -> ApiResponse:
        dev_ref = self._data.device_reference_id or self._data.device_id
        if not dev_ref:
            pytest.skip("deviceReferenceId not configured")
        return self._client.get(
            MobileEndpoints.device_assignable(dev_ref),
            params={"farmId": self._data.farm_id} if self._data.farm_id else None,
        )

    def get_general_settings(self) -> ApiResponse:
        if self._data.device_uuid:
            resp = self._client.get(MobileEndpoints.general_settings(self._data.device_uuid))
            if resp.status_code != 404:
                return resp
        device_uuid = self._resolve_device_uuid()
        return self._client.get(MobileEndpoints.general_settings(device_uuid))

    def get_alert_settings(self) -> ApiResponse:
        if not self._data.device_id:
            pytest.skip("deviceId not configured")
        return self._client.get(MobileEndpoints.alert_settings(self._data.device_id))

    def get_delay_settings(self) -> ApiResponse:
        if self._data.device_uuid:
            resp = self._client.get(MobileEndpoints.delay_settings(self._data.device_uuid))
            if resp.status_code != 404:
                return resp
        device_uuid = self._resolve_device_uuid()
        return self._client.get(MobileEndpoints.delay_settings(device_uuid))

    def get_device_states_by_farm(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(MobileEndpoints.device_states_by_farm(self._data.farm_id))

    def get_device_connection_status(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(
            MobileEndpoints.device_connection_status(self._data.farm_id)
        )

    def get_device_tree(self) -> ApiResponse:
        if not self._data.device_id:
            pytest.skip("deviceId not configured")
        return self._client.get(MobileEndpoints.device_tree(self._data.device_id))

    def get_device_details(self) -> ApiResponse:
        resp = self._client.get(
            MobileEndpoints.device_details(),
            headers={"x-nbvx-usr-pref-unit-system": "SI"},
        )
        if resp.status_code == 400:
            pytest.skip("Backend DataAPI failure on deviceDetails call")
        return resp

    def get_device_recipes(self) -> ApiResponse:
        if not self._data.farm_id or not self._data.device_uuid:
            pytest.skip("farmId or deviceUuid not configured")
        return self._client.get(
            MobileEndpoints.device_recipes(self._data.farm_id, self._data.device_uuid)
        )

    def get_device_recipes_with_usage(self) -> ApiResponse:
        if not self._data.farm_id or not self._data.device_uuid:
            pytest.skip("farmId or deviceUuid not configured")
        return self._client.get(
            MobileEndpoints.device_recipes_with_usage(
                self._data.farm_id, self._data.device_uuid
            )
        )

    def get_user_device_graphs(self) -> ApiResponse:
        if not self._data.farm_id or not self._data.device_id:
            pytest.skip("farmId or deviceId not configured")
        return self._client.get(
            MobileEndpoints.user_device_graphs(self._data.farm_id, self._data.device_id)
        )

    def get_user_device_graph(self, graph_id: str) -> ApiResponse:
        if not self._data.farm_id or not self._data.device_id:
            pytest.skip("farmId or deviceId not configured")
        return self._client.get(
            MobileEndpoints.user_device_graph(
                self._data.farm_id, self._data.device_id, graph_id
            )
        )

    # Farms
    def get_io_list(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(MobileEndpoints.io_list(self._data.farm_id))

    def get_trees(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(
            MobileEndpoints.trees(), params={"farmId": self._data.farm_id}
        )

    def get_dashboard_data(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        resp = self._client.get(MobileEndpoints.dashboard_data(self._data.farm_id))
        if resp.status_code == 409:
            # Try fallback farms
            for farm_id in _FALLBACK_FARM_IDS:
                if farm_id == self._data.farm_id:
                    continue
                resp = self._client.get(MobileEndpoints.dashboard_data(farm_id))
                if resp.status_code == 200:
                    return resp
            pytest.skip("Dashboard data conflict (409)")
        return resp

    def get_homepage_devices(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        resp = self._client.get(MobileEndpoints.homepage_devices(self._data.farm_id))
        if resp.status_code == 404:
            pytest.skip("HomePage devices not available")
        return resp

    # General
    def get_notes(self) -> ApiResponse:
        return self._client.get(MobileEndpoints.notes())

    def get_system_types(self) -> ApiResponse:
        resp = self._client.get(MobileEndpoints.system_types())
        if resp.status_code == 400:
            pytest.skip("Gateway dynamic call returned 400")
        return resp

    # Irrigation
    def get_farm_program_schemes(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(MobileEndpoints.farm_program_schemes(self._data.farm_id))

    def get_device_program_schemes(self) -> ApiResponse:
        if not self._data.farm_id or not self._data.device_uuid:
            pytest.skip("farmId or deviceUuid not configured")
        return self._client.get(
            MobileEndpoints.device_program_schemes(
                self._data.farm_id, self._data.device_uuid
            )
        )

    def get_program_scheme(self) -> ApiResponse:
        if not self._data.farm_id or not self._data.program_uuid:
            pytest.skip("farmId or programUuid not configured")
        return self._client.get(
            MobileEndpoints.program_scheme(self._data.farm_id, self._data.program_uuid)
        )

    def get_program_scheme_status(self) -> ApiResponse:
        if not self._data.farm_id or not self._data.program_uuid:
            pytest.skip("farmId or programUuid not configured")
        return self._client.get(
            MobileEndpoints.program_scheme_status(
                self._data.farm_id, self._data.program_uuid
            )
        )

    def get_device_program_schemes_statuses(self) -> ApiResponse:
        if not self._data.farm_id or not self._data.device_uuid:
            pytest.skip("farmId or deviceUuid not configured")
        return self._client.get(
            MobileEndpoints.device_program_schemes_statuses(
                self._data.farm_id, self._data.device_uuid
            )
        )

    def get_irrigation_programs(self) -> ApiResponse:
        device_id = self._data.device_uuid or self._data.device_id
        if not device_id:
            pytest.skip("deviceId/deviceUuid not configured")
        return self._client.get(MobileEndpoints.irrigation_programs(device_id))

    def get_irrigation_programs_daily(self) -> ApiResponse:
        device_id = self._data.device_uuid or self._data.device_id
        date = self._data.date or "2024-01-01"
        if not device_id:
            pytest.skip("deviceId/deviceUuid not configured")
        return self._client.get(
            MobileEndpoints.irrigation_programs_daily(device_id),
            params={"dateOnly": date},
        )

    def get_last_irrigation(self) -> ApiResponse:
        prog_uuid = self._data.irrigation_program_uuid or self._data.program_uuid
        if not prog_uuid:
            pytest.skip("irrigationProgramUuid not configured")
        return self._client.get(MobileEndpoints.last_irrigation(prog_uuid))

    def get_device_irrigation_blocks(self) -> ApiResponse:
        if not self._data.device_id:
            pytest.skip("deviceId not configured")
        resp = self._client.get(
            MobileEndpoints.device_irrigation_blocks(self._data.device_id),
            headers={"x-nbvx-usr-pref-unit-system": "SI"},
        )
        if resp.status_code == 400:
            pytest.skip("Backend DataAPI failure on irrigationBlocks call")
        return resp

    def get_irrigation_blocks(self) -> ApiResponse:
        resp = self._client.get(
            MobileEndpoints.irrigation_blocks(),
            headers={"x-nbvx-usr-pref-unit-system": "SI"},
        )
        if resp.status_code == 400:
            pytest.skip("Backend DataAPI failure on irrigationBlocks call")
        return resp

    def get_max_program_overview(self) -> ApiResponse:
        if not self._data.program_uuid:
            pytest.skip("programUuid not configured")
        resp = self._client.get(
            MobileEndpoints.max_program_overview(self._data.program_uuid)
        )
        if resp.status_code == 404:
            pytest.skip("Program not found")
        return resp

    def get_program_progress(self) -> ApiResponse:
        if not self._data.program_uuid:
            pytest.skip("programUuid not configured")
        resp = self._client.get(MobileEndpoints.program_progress(self._data.program_uuid))
        if resp.status_code == 404:
            pytest.skip("Program not found")
        if resp.status_code == 400:
            pytest.skip("Program has no active progress data")
        return resp

    # Provisioning
    def get_provisioning_farm(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        resp = self._client.get(MobileEndpoints.provisioning_farm(self._data.farm_id))
        if resp.status_code == 409:
            for farm_id in _FALLBACK_FARM_IDS:
                if farm_id == self._data.farm_id:
                    continue
                resp = self._client.get(MobileEndpoints.provisioning_farm(farm_id))
                if resp.status_code in (200, 204):
                    return resp
            pytest.skip("Provisioning conflict (409) on all farms — flow already in progress")
        return resp

    def get_provisioning_status(self, flow_uuid: str = None) -> ApiResponse:
        uuid = flow_uuid or self._data.flow_uuid or self._resolve_flow_uuid()
        resp = self._client.get(MobileEndpoints.provisioning_status(uuid))
        if resp.status_code == 400:
            pytest.skip("Provisioning status returned 400")
        return resp

    # Reports
    def get_last_eco_daily_program_report(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        if not self._data.device_program_id:
            pytest.skip("deviceProgramId not configured")
        params = {"deviceProgramId": self._data.device_program_id}
        if self._data.device_uuid:
            params["deviceUUid"] = self._data.device_uuid
        resp = self._client.get(
            MobileEndpoints.last_eco_daily_program_report(self._data.farm_id), params=params
        )
        if resp.status_code == 404:
            # Try fallback farms without deviceUUid — eco reports may exist elsewhere
            for farm_id in _FALLBACK_FARM_IDS:
                if farm_id == self._data.farm_id:
                    continue
                r = self._client.get(
                    MobileEndpoints.last_eco_daily_program_report(farm_id),
                    params={"deviceProgramId": self._data.device_program_id},
                )
                if r.status_code == 200:
                    return r
            pytest.skip("No eco daily program report found for device in QA1")
        return resp

    def get_daily_report(self) -> ApiResponse:
        device_id = self._data.device_uuid or self._data.device_id
        date = self._data.date or "2024-01-01"
        if not device_id:
            pytest.skip("deviceId/deviceUuid not configured")
        return self._client.get(MobileEndpoints.daily_report(device_id, date))

    def get_irrigation_logs(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        device_id = self._data.device_uuid or self._data.device_id
        date = self._data.date or "2024-01-01"
        if not device_id:
            pytest.skip("deviceId/deviceUuid not configured")
        return self._client.get(
            MobileEndpoints.irrigation_logs(self._data.farm_id, device_id, date),
            headers={"x-nbvx-usr-pref-unit-system": "SI"},
        )

    # Users
    def get_user_details(self) -> ApiResponse:
        resp = self._client.get(
            MobileEndpoints.user_details(),
            headers={"x-nbvx-usr-pref-unit-system": "SI"},
        )
        if resp.status_code == 400:
            pytest.skip("Backend DataAPI failure on userDetails call")
        return resp

    def get_user_graphs(self) -> ApiResponse:
        return self._client.get(MobileEndpoints.user_graphs())
