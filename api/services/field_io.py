import pytest
from api.client.api_client import QAApiClient
from api.client.response import ApiResponse
from api.endpoints.field_io import FieldIOEndpoints


class FieldIOService:
    def __init__(self, client: QAApiClient, data):
        self._client = client
        self._data = data

    # Bases
    def get_bases(self) -> ApiResponse:
        params = {"farmId": self._data.farm_id} if self._data.farm_id else None
        return self._client.get(FieldIOEndpoints.bases(), params=params)

    def get_bases_address(self) -> ApiResponse:
        params = {"farmId": self._data.farm_id} if self._data.farm_id else None
        return self._client.get(FieldIOEndpoints.bases_address(), params=params)

    def get_base(self) -> ApiResponse:
        if not self._data.base_id:
            pytest.skip("baseId not configured")
        return self._client.get(FieldIOEndpoints.base(self._data.base_id))

    def get_base_address(self) -> ApiResponse:
        if not self._data.base_id:
            pytest.skip("baseId not configured")
        return self._client.get(FieldIOEndpoints.base_address(self._data.base_id))

    def get_bases_by_system_type(self) -> ApiResponse:
        params = {
            "farmId": self._data.farm_id,
            "systemTypeId": self._data.system_type_id,
        }
        return self._client.get(FieldIOEndpoints.bases_by_system_type(), params=params)

    # Connections
    def get_davis_ws_connections(self) -> ApiResponse:
        params = {"farmId": self._data.farm_id} if self._data.farm_id else None
        return self._client.get(FieldIOEndpoints.davis_ws_connections(), params=params)

    # Devices
    def get_devices(self) -> ApiResponse:
        params = {"farmIds": self._data.farm_id} if self._data.farm_id else None
        return self._client.get(FieldIOEndpoints.devices(), params=params)

    def get_device(self) -> ApiResponse:
        if not self._data.device_reference_id:
            pytest.skip("deviceReferenceId not configured")
        return self._client.get(FieldIOEndpoints.device(self._data.device_reference_id))

    def get_device_address(self) -> ApiResponse:
        if not self._data.device_reference_id:
            pytest.skip("deviceReferenceId not configured")
        return self._client.get(
            FieldIOEndpoints.device_address(self._data.device_reference_id)
        )

    # Icons
    def get_icons(self) -> ApiResponse:
        return self._client.get(FieldIOEndpoints.icons())

    # IO
    def get_io(self) -> ApiResponse:
        if not self._data.io_id:
            pytest.skip("ioId not configured")
        return self._client.get(FieldIOEndpoints.io(self._data.io_id))

    def get_ios(self) -> ApiResponse:
        params = {"farmId": self._data.farm_id} if self._data.farm_id else None
        return self._client.get(FieldIOEndpoints.ios(), params=params)

    # IoDeviceTypes
    def get_io_device_types(self) -> ApiResponse:
        return self._client.get(FieldIOEndpoints.io_device_types())

    def get_io_device_type(self) -> ApiResponse:
        if not self._data.io_device_type_id:
            pytest.skip("ioDeviceTypeId not configured")
        return self._client.get(
            FieldIOEndpoints.io_device_type(self._data.io_device_type_id)
        )

    # IoGroups
    def get_io_group(self) -> ApiResponse:
        if not self._data.io_group_id:
            pytest.skip("ioGroupId not configured")
        return self._client.get(FieldIOEndpoints.io_group(self._data.io_group_id))

    def get_io_groups(self) -> ApiResponse:
        params = {"farmId": self._data.farm_id} if self._data.farm_id else None
        return self._client.get(FieldIOEndpoints.io_groups(), params=params)

    # IoTypes
    def get_io_types(self) -> ApiResponse:
        return self._client.get(FieldIOEndpoints.io_types())

    def get_io_type(self) -> ApiResponse:
        if not self._data.io_type_id:
            pytest.skip("ioTypeId not configured")
        return self._client.get(FieldIOEndpoints.io_type(self._data.io_type_id))

    # Remotes
    def get_remotes(self) -> ApiResponse:
        params = {"farmId": self._data.farm_id} if self._data.farm_id else None
        return self._client.get(FieldIOEndpoints.remotes(), params=params)

    def get_remote(self) -> ApiResponse:
        if not self._data.remote_id:
            pytest.skip("remoteId not configured")
        return self._client.get(FieldIOEndpoints.remote(self._data.remote_id))

    # Repeaters
    def get_repeaters(self) -> ApiResponse:
        params = {"farmId": self._data.farm_id} if self._data.farm_id else None
        return self._client.get(FieldIOEndpoints.repeaters(), params=params)

    _FALLBACK_FARM_IDS = [
        "qa1-nb10047", "qa1-nb14218", "qa1-nb10058", "qa1-nb11141", "qa1-nb13042",
        "qa1-nb14595", "qa1-nb14604", "qa1-nb14644", "qa1-nb14658", "qa1-nb14677",
        "qa1-nb14716", "qa1-nb14752", "qa1-nb14753", "qa1-nb14776", "qa1-nb14781",
        "qa1-nb14900", "qa1-nb14905", "qa1-nb14948", "qa1-nb14952", "qa1-nb15017",
        "qa1-nb15116", "qa1-nb15214", "qa1-nb15551", "qa1-nb15778", "qa1-nb10000",
    ]

    def _resolve_repeater_id(self) -> str:
        if '_repeater_id' not in self.__dict__:
            tried = []
            for farm_id in self._FALLBACK_FARM_IDS:
                resp = self._client.get(FieldIOEndpoints.repeaters(), params={"farmId": farm_id})
                if resp.status_code != 200:
                    tried.append(farm_id)
                    continue
                data = resp.json()
                items = data if isinstance(data, list) else data.get('repeaters', data.get('items', []))
                if items:
                    self._repeater_id = items[0].get('id') or items[0].get('repeaterId')
                    return self._repeater_id
                tried.append(farm_id)
            pytest.skip(f"No Repeaters found in any farm (tried: {tried})")
        return self._repeater_id

    def get_repeater(self) -> ApiResponse:
        repeater_id = self._data.repeater_id or self._resolve_repeater_id()
        return self._client.get(FieldIOEndpoints.repeater(repeater_id))

    # SystemTypes
    def get_system_types(self) -> ApiResponse:
        return self._client.get(FieldIOEndpoints.system_types())

    def get_system_type(self) -> ApiResponse:
        if not self._data.system_type_id:
            pytest.skip("systemTypeId not configured")
        return self._client.get(FieldIOEndpoints.system_type(self._data.system_type_id))

    # Thresholds
    def get_thresholds(self) -> ApiResponse:
        params = {"farmId": self._data.farm_id} if self._data.farm_id else None
        return self._client.get(FieldIOEndpoints.thresholds(), params=params)

    # Trees
    def get_base_tree(self) -> ApiResponse:
        if not self._data.base_id:
            pytest.skip("baseId not configured")
        return self._client.get(FieldIOEndpoints.base_tree(self._data.base_id))

    def get_device_tree(self) -> ApiResponse:
        if not self._data.device_reference_id:
            pytest.skip("deviceReferenceId not configured")
        return self._client.get(FieldIOEndpoints.device_tree(self._data.device_reference_id))

    def get_farm_trees(self) -> ApiResponse:
        params = {"farmId": self._data.farm_id} if self._data.farm_id else None
        return self._client.get(FieldIOEndpoints.farm_trees(), params=params)

    def get_device_tree_lite(self) -> ApiResponse:
        if not self._data.device_reference_id:
            pytest.skip("deviceReferenceId not configured")
        return self._client.get(
            FieldIOEndpoints.device_tree_lite(self._data.device_reference_id)
        )
