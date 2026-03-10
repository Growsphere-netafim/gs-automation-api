import pytest
from api.client.api_client import QAApiClient
from api.client.response import ApiResponse
from api.endpoints.commands_manager import CommandsManagerEndpoints


class CommandsManagerService:
    def __init__(self, client: QAApiClient, data):
        self._client = client
        self._data = data

    def _resolve_reference_id(self) -> str:
        if '_reference_id' not in self.__dict__:
            resp = self._client.get(
                CommandsManagerEndpoints.odata_commands_global(), params={"$top": 10}
            )
            if resp.status_code == 200:
                data = resp.json()
                items = data.get('value', []) if isinstance(data, dict) else data
                for item in (items if isinstance(items, list) else []):
                    ref_id = item.get('referenceId')
                    if ref_id:
                        self._reference_id = ref_id
                        return ref_id
            pytest.skip("No command referenceId found via OData")
        return self._reference_id

    def get_command_status(self) -> ApiResponse:
        reference_id = self._data.reference_id or self._resolve_reference_id()
        return self._client.get(
            CommandsManagerEndpoints.command_status(reference_id)
        )

    def get_latest_statuses_farm(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(
            CommandsManagerEndpoints.latest_statuses_farm(self._data.farm_id)
        )

    def get_latest_statuses_global(self) -> ApiResponse:
        params = {"farmId": self._data.farm_id} if self._data.farm_id else None
        return self._client.get(
            CommandsManagerEndpoints.latest_statuses_global(), params=params
        )

    def get_device_request_latest(self) -> ApiResponse:
        if not self._data.device_id:
            pytest.skip("deviceId not configured")
        if not self._data.reference_id:
            pytest.skip("referenceId (requestId) not configured")
        return self._client.get(
            CommandsManagerEndpoints.device_request_latest(
                self._data.device_id, self._data.reference_id
            )
        )

    def get_odata_commands_global(self) -> ApiResponse:
        return self._client.get(
            CommandsManagerEndpoints.odata_commands_global(), params={"$top": 10}
        )

    def get_odata_commands_farm(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        resp = self._client.get(
            CommandsManagerEndpoints.odata_commands_farm(self._data.farm_id),
            params={"$top": 10},
        )
        if resp.status_code == 403:
            pytest.skip("OData Commands forbidden for this farm (403)")
        return resp
