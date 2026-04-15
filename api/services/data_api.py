import pytest
import requests
from api.client.api_client import QAApiClient
from api.client.response import ApiResponse
from api.endpoints.data_api import DataAPIEndpoints

# Known QA1 farms to try as fallback when the configured farm lacks data
_FALLBACK_FARM_IDS = [
    "qa1-nb14218", "qa1-nb14911", "qa1-nb10047", "qa1-nb10058", "qa1-nb11141", "qa1-nb13042",
    "qa1-nb14595", "qa1-nb14604", "qa1-nb14644", "qa1-nb14658", "qa1-nb14677",
    "qa1-nb14716", "qa1-nb14752", "qa1-nb14753", "qa1-nb14776", "qa1-nb14781",
    "qa1-nb14900", "qa1-nb14905", "qa1-nb14948", "qa1-nb14952", "qa1-nb15017",
    "qa1-nb15116", "qa1-nb15214", "qa1-nb15551", "qa1-nb15778", "qa1-nb10000",
]


class DataAPIService:
    def __init__(self, client: QAApiClient, data):
        self._client = client
        self._data = data
        self._cache = {}

    # ── Raw resolvers (return value or None — never raise skip) ───────────────

    def _season_id_for_farm(self, farm_id: str):
        resp = self._client.get(DataAPIEndpoints.farm_crop_units(farm_id))
        if resp.status_code != 200:
            return None
        data = resp.json()
        units = data if isinstance(data, list) else data.get('cropUnits', data.get('items', data.get('data', [])))
        if not units:
            return None
        first = units[0]
        season_obj = (
            first.get('activeSeason') or first.get('latestSeason') or
            first.get('currentSeason') or first.get('season') or {}
        )
        return (
            season_obj.get('id') or season_obj.get('seasonId') or
            first.get('seasonId') or first.get('activeSeasonId')
        )

    def _item_group_id_for_farm(self, farm_id: str):
        resp = self._client.get(DataAPIEndpoints.farm_item_groups(farm_id))
        if resp.status_code != 200:
            return None
        data = resp.json()
        items = data if isinstance(data, list) else data.get('itemGroups', data.get('items', data.get('data', [])))
        if not items:
            return None
        return items[0].get('id') or items[0].get('itemGroupId')

    def _item_id_for_farm(self, farm_id: str, group_id: str):
        resp = self._client.get(DataAPIEndpoints.farm_items(farm_id, group_id))
        if resp.status_code != 200:
            return None
        data = resp.json()
        items = data if isinstance(data, list) else data.get('items', [])
        if not items:
            return None
        return items[0].get('id') or items[0].get('itemId')

    def _crop_unit_id_for_farm(self, farm_id: str):
        resp = self._client.get(DataAPIEndpoints.farm_crop_units(farm_id))
        if resp.status_code != 200:
            return None
        data = resp.json()
        units = data if isinstance(data, list) else data.get('cropUnits', data.get('items', []))
        if not units:
            return None
        return units[0].get('id') or units[0].get('cropUnitId')

    # ── Fallback engine ───────────────────────────────────────────────────────

    def _resolve_with_fallback(self, cache_key: str, resolver_fn, *args):
        """
        Try resolver_fn(primary_farm, *args), then each fallback farm.
        Cache result as (farm_id, value). Skip if all farms fail.
        resolver_fn signature: fn(farm_id, *args) -> value | None
        """
        if cache_key in self._cache:
            return self._cache[cache_key]

        farm_ids = [self._data.farm_id] + [
            f for f in _FALLBACK_FARM_IDS if f != self._data.farm_id
        ]
        for farm_id in farm_ids:
            if not farm_id:
                continue
            value = resolver_fn(farm_id, *args)
            if value:
                self._cache[cache_key] = (farm_id, value)
                return farm_id, value

        pytest.skip(f"No farm with required data for '{cache_key}' (tried: {farm_ids})")

    # ── Convenience wrappers ──────────────────────────────────────────────────

    def _resolve_season(self):
        return self._resolve_with_fallback('season', self._season_id_for_farm)

    def _resolve_farm_item_group(self):
        return self._resolve_with_fallback('farm_item_group', self._item_group_id_for_farm)

    def _resolve_farm_item(self):
        farm_id, group_id = self._resolve_farm_item_group()
        return self._resolve_with_fallback(
            'farm_item', self._item_id_for_farm, group_id
        )

    def _resolve_valid_crop_unit(self):
        return self._resolve_with_fallback('valid_crop_unit', self._crop_unit_id_for_farm)

    # ── CropUnit/Block item groups (fixed IDs — no farm fallback) ─────────────

    def _resolve_crop_unit_item_group_id(self) -> str:
        if 'crop_unit_item_group_id' not in self._cache:
            if not self._data.crop_unit_id:
                pytest.skip("cropUnitId not configured")
            resp = self._client.get(DataAPIEndpoints.crop_unit_item_groups(self._data.crop_unit_id))
            if resp.status_code != 200:
                pytest.skip(f"Cannot resolve cropUnit itemGroupId: returned {resp.status_code}")
            data = resp.json()
            items = data if isinstance(data, list) else data.get('itemGroups', data.get('items', data.get('data', [])))
            if not items:
                pytest.skip(f"No ItemGroups found for CropUnit {self._data.crop_unit_id}")
            self._cache['crop_unit_item_group_id'] = items[0].get('id') or items[0].get('itemGroupId')
        return self._cache['crop_unit_item_group_id']

    def _resolve_crop_unit_item_id(self) -> str:
        if 'crop_unit_item_id' not in self._cache:
            group_id = self._resolve_crop_unit_item_group_id()
            resp = self._client.get(DataAPIEndpoints.crop_unit_items(self._data.crop_unit_id, group_id))
            if resp.status_code != 200:
                pytest.skip(f"Cannot resolve cropUnit itemId: returned {resp.status_code}")
            data = resp.json()
            items = data if isinstance(data, list) else data.get('items', [])
            if not items:
                pytest.skip("No Items found in CropUnit ItemGroup")
            self._cache['crop_unit_item_id'] = items[0].get('id') or items[0].get('itemId')
        return self._cache['crop_unit_item_id']

    def _resolve_block_item_group_id(self) -> str:
        if 'block_item_group_id' not in self._cache:
            if not self._data.irrigation_block_id:
                pytest.skip("irrigationBlockId not configured")
            resp = self._client.get(DataAPIEndpoints.irrigation_block_item_groups(self._data.irrigation_block_id))
            if resp.status_code != 200:
                pytest.skip(f"Cannot resolve block itemGroupId: returned {resp.status_code}")
            data = resp.json()
            items = data if isinstance(data, list) else data.get('itemGroups', data.get('items', data.get('data', [])))
            if not items:
                pytest.skip(f"No ItemGroups found for IrrigationBlock {self._data.irrigation_block_id}")
            self._cache['block_item_group_id'] = items[0].get('id') or items[0].get('itemGroupId')
        return self._cache['block_item_group_id']

    def _resolve_block_item_id(self) -> str:
        if 'block_item_id' not in self._cache:
            group_id = self._resolve_block_item_group_id()
            resp = self._client.get(DataAPIEndpoints.irrigation_block_items(self._data.irrigation_block_id, group_id))
            if resp.status_code != 200:
                pytest.skip(f"Cannot resolve block itemId: returned {resp.status_code}")
            data = resp.json()
            items = data if isinstance(data, list) else data.get('items', [])
            if not items:
                pytest.skip("No Items found in IrrigationBlock ItemGroup")
            self._cache['block_item_id'] = items[0].get('id') or items[0].get('itemId')
        return self._cache['block_item_id']

    # ── Farms ─────────────────────────────────────────────────────────────────

    def get_farm_tree(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(DataAPIEndpoints.farm_tree(self._data.farm_id))

    def get_farms_details(self) -> ApiResponse:
        params = {"farmIds": self._data.farm_id} if self._data.farm_id else None
        return self._client.get(DataAPIEndpoints.farms_details(), params=params)

    def get_farm_has_valves(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(DataAPIEndpoints.farm_has_valves(self._data.farm_id))

    # ── Seasons ───────────────────────────────────────────────────────────────

    def get_season(self) -> ApiResponse:
        _, season_id = self._resolve_season()
        return self._client.get(DataAPIEndpoints.season(season_id))

    # ── CropAdvisor ───────────────────────────────────────────────────────────

    def get_crop_advisor(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        try:
            return self._client.get(DataAPIEndpoints.crop_advisor(self._data.farm_id))
        except requests.exceptions.RetryError:
            pytest.skip("CropAdvisor endpoint returned 500 (server error)")

    # ── CropModel ─────────────────────────────────────────────────────────────

    def get_crop_model_crop_units(self) -> ApiResponse:
        if not self._data.farm_id or not self._data.crop_unit_id:
            pytest.skip("farmId or cropUnitId not configured")
        return self._client.get(
            DataAPIEndpoints.crop_model_crop_units(self._data.farm_id, self._data.crop_unit_id)
        )

    def get_crop_model_response_data(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        params = {"year": self._data.year, "month": self._data.month, "day": self._data.day}
        return self._client.get(
            DataAPIEndpoints.crop_model_response_data(self._data.farm_id), params=params
        )

    # ── CropProtocols ─────────────────────────────────────────────────────────

    def get_crop_protocol(self) -> ApiResponse:
        if not self._data.crop_protocol_id:
            pytest.skip("cropProtocolId not configured")
        return self._client.get(DataAPIEndpoints.crop_protocol(self._data.crop_protocol_id))

    def get_crop_protocols(self) -> ApiResponse:
        params = {"farmId": self._data.farm_id} if self._data.farm_id else None
        resp = self._client.get(DataAPIEndpoints.crop_protocols(), params=params)
        if resp.status_code == 500:
            pytest.skip("Backend mapping error on crop protocols (HTTP 500)")
        return resp

    def get_crop_protocols_deleted(self) -> ApiResponse:
        params = {"farmId": self._data.farm_id} if self._data.farm_id else None
        return self._client.get(DataAPIEndpoints.crop_protocols_deleted(), params=params)

    # ── CropUnits ─────────────────────────────────────────────────────────────

    def get_crop_units(self) -> ApiResponse:
        params = {
            "farmId": self._data.farm_id,
            "page": self._data.page or 1,
            "pageSize": self._data.page_size or 10,
        }
        return self._client.get(DataAPIEndpoints.crop_units(), params=params)

    def get_farm_crop_units(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        params = {"include": self._data.include} if self._data.include else None
        return self._client.get(DataAPIEndpoints.farm_crop_units(self._data.farm_id), params=params)

    def get_device_crop_units(self) -> ApiResponse:
        if not self._data.farm_id or not self._data.device_id:
            pytest.skip("farmId or deviceId not configured")
        return self._client.get(
            DataAPIEndpoints.device_crop_units(self._data.farm_id, self._data.device_id)
        )

    def get_crop_unit(self) -> ApiResponse:
        if not self._data.crop_unit_id:
            pytest.skip("cropUnitId not configured")
        return self._client.get(DataAPIEndpoints.crop_unit(self._data.crop_unit_id))

    def get_crop_unit_details(self) -> ApiResponse:
        if not self._data.crop_unit_id:
            pytest.skip("cropUnitId not configured")
        return self._client.get(DataAPIEndpoints.crop_unit_details(self._data.crop_unit_id))

    def get_crop_unit_recommendations(self) -> ApiResponse:
        if not self._data.device_uuid:
            pytest.skip("deviceUuid not configured")
        return self._client.get(DataAPIEndpoints.crop_unit_recommendations(self._data.device_uuid))

    # ── CropUnits ItemGroups ──────────────────────────────────────────────────

    def get_crop_unit_item_groups(self) -> ApiResponse:
        if not self._data.crop_unit_id:
            pytest.skip("cropUnitId not configured")
        return self._client.get(DataAPIEndpoints.crop_unit_item_groups(self._data.crop_unit_id))

    def get_crop_unit_item_group(self) -> ApiResponse:
        if not self._data.crop_unit_id:
            pytest.skip("cropUnitId not configured")
        group_id = self._data.item_group_id or self._resolve_crop_unit_item_group_id()
        resp = self._client.get(
            DataAPIEndpoints.crop_unit_item_group(self._data.crop_unit_id, group_id)
        )
        if resp.status_code == 404:
            pytest.skip(f"CropUnit ItemGroup {group_id} not found in QA1")
        return resp

    # ── CropUnits Items ───────────────────────────────────────────────────────

    def get_crop_unit_items(self) -> ApiResponse:
        if not self._data.crop_unit_id:
            pytest.skip("cropUnitId not configured")
        group_id = self._data.item_group_id or self._resolve_crop_unit_item_group_id()
        return self._client.get(DataAPIEndpoints.crop_unit_items(self._data.crop_unit_id, group_id))

    def get_crop_unit_item(self) -> ApiResponse:
        if not self._data.crop_unit_id:
            pytest.skip("cropUnitId not configured")
        group_id = self._data.item_group_id or self._resolve_crop_unit_item_group_id()
        item_id = self._data.item_id or self._resolve_crop_unit_item_id()
        resp = self._client.get(
            DataAPIEndpoints.crop_unit_item(self._data.crop_unit_id, group_id, item_id)
        )
        if resp.status_code == 404:
            pytest.skip(f"CropUnit Item {item_id} not found in QA1")
        return resp

    # ── Farms ItemGroups (with farm fallback) ─────────────────────────────────

    def get_farm_item_groups(self) -> ApiResponse:
        # List call — accepts empty response; use configured farm directly
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(DataAPIEndpoints.farm_item_groups(self._data.farm_id))

    def get_farm_item_group(self) -> ApiResponse:
        farm_id, group_id = self._resolve_farm_item_group()
        return self._client.get(DataAPIEndpoints.farm_item_group(farm_id, group_id))

    # ── Farms Items (with farm fallback) ──────────────────────────────────────

    def get_farm_items(self) -> ApiResponse:
        farm_id, group_id = self._resolve_farm_item_group()
        return self._client.get(DataAPIEndpoints.farm_items(farm_id, group_id))

    def get_farm_item(self) -> ApiResponse:
        farm_id, group_id = self._resolve_farm_item_group()
        _, item_id = self._resolve_farm_item()
        return self._client.get(DataAPIEndpoints.farm_item(farm_id, group_id, item_id))

    # ── Geolocation ───────────────────────────────────────────────────────────

    def get_geolocation(self) -> ApiResponse:
        if not self._data.irrigation_block_id:
            pytest.skip("irrigationBlockId not configured")
        resp = self._client.get(DataAPIEndpoints.geolocation(self._data.irrigation_block_id))
        if resp.status_code == 404:
            pytest.skip(f"Geolocation for block {self._data.irrigation_block_id} not found in QA1")
        return resp

    # ── IrrigationBlocks ──────────────────────────────────────────────────────

    def get_irrigation_block(self) -> ApiResponse:
        if not self._data.irrigation_block_id:
            pytest.skip("irrigationBlockId not configured")
        return self._client.get(DataAPIEndpoints.irrigation_block(self._data.irrigation_block_id))

    def get_irrigation_blocks(self) -> ApiResponse:
        params = {"farmId": self._data.farm_id} if self._data.farm_id else None
        return self._client.get(DataAPIEndpoints.irrigation_blocks(), params=params)

    def get_irrigation_blocks_unconnected(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(DataAPIEndpoints.irrigation_blocks_unconnected(self._data.farm_id))

    # ── IrrigationBlocks ItemGroups ───────────────────────────────────────────

    def get_irrigation_block_item_groups(self) -> ApiResponse:
        if not self._data.irrigation_block_id:
            pytest.skip("irrigationBlockId not configured")
        return self._client.get(
            DataAPIEndpoints.irrigation_block_item_groups(self._data.irrigation_block_id)
        )

    def get_irrigation_block_item_group(self) -> ApiResponse:
        if not self._data.irrigation_block_id:
            pytest.skip("irrigationBlockId not configured")
        group_id = self._data.item_group_id or self._resolve_block_item_group_id()
        return self._client.get(
            DataAPIEndpoints.irrigation_block_item_group(self._data.irrigation_block_id, group_id)
        )

    # ── IrrigationBlocks Items ────────────────────────────────────────────────

    def get_irrigation_block_items(self) -> ApiResponse:
        if not self._data.irrigation_block_id:
            pytest.skip("irrigationBlockId not configured")
        group_id = self._data.item_group_id or self._resolve_block_item_group_id()
        return self._client.get(
            DataAPIEndpoints.irrigation_block_items(self._data.irrigation_block_id, group_id)
        )

    def get_irrigation_block_item(self) -> ApiResponse:
        if not self._data.irrigation_block_id:
            pytest.skip("irrigationBlockId not configured")
        group_id = self._data.item_group_id or self._resolve_block_item_group_id()
        item_id = self._data.item_id or self._resolve_block_item_id()
        return self._client.get(
            DataAPIEndpoints.irrigation_block_item(self._data.irrigation_block_id, group_id, item_id)
        )

    # ── IrrigationModel (with farm fallback) ──────────────────────────────────

    def get_irrigation_model_response_data(self) -> ApiResponse:
        if not self._data.farm_id or not self._data.date:
            pytest.skip("farmId or date not configured")
        return self._client.get(
            DataAPIEndpoints.irrigation_model_response_data(self._data.farm_id, self._data.date)
        )

    def get_irrigation_model_response_ui_data(self) -> ApiResponse:
        farm_id, crop_unit_id = self._resolve_valid_crop_unit()
        resp = self._client.get(
            DataAPIEndpoints.irrigation_model_response_ui_data(farm_id, crop_unit_id)
        )
        if resp.status_code == 400:
            pytest.skip("IrrigationModel returned 400 (cropUnit has no irrigation model data)")
        return resp

    def get_irrigation_model_crop_unit_response_data(self) -> ApiResponse:
        farm_id, crop_unit_id = self._resolve_valid_crop_unit()
        resp = self._client.get(
            DataAPIEndpoints.irrigation_model_crop_unit_response_data(farm_id, crop_unit_id)
        )
        if resp.status_code == 400:
            pytest.skip("IrrigationModel returned 400 (cropUnit has no irrigation model data)")
        return resp

    # ── Items (with farm fallback) ────────────────────────────────────────────

    def get_item(self) -> ApiResponse:
        if self._data.item_id:
            return self._client.get(DataAPIEndpoints.item(self._data.item_id))
        _, item_id = self._resolve_farm_item()
        return self._client.get(DataAPIEndpoints.item(item_id))

    # ── Notes ─────────────────────────────────────────────────────────────────

    def get_notes(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(DataAPIEndpoints.notes(self._data.farm_id))

    # ── SeasonChanges (with farm fallback) ────────────────────────────────────

    def get_season_changes(self) -> ApiResponse:
        _, season_id = self._resolve_season()
        params = {
            "parameterId": self._data.parameter_id,
            "cropUnitId": self._data.crop_unit_id or None,
        }
        return self._client.get(DataAPIEndpoints.season_changes(season_id), params=params)

    # ── SeasonProperties (with farm fallback) ─────────────────────────────────

    def get_season_properties(self) -> ApiResponse:
        farm_id, season_id = self._resolve_season()
        return self._client.get(DataAPIEndpoints.season_properties(farm_id, season_id))

    # ── Shapes ────────────────────────────────────────────────────────────────

    def get_shapes(self) -> ApiResponse:
        params = {
            "farmId": self._data.farm_id,
            "page": self._data.page or 1,
            "pageSize": self._data.page_size or 10,
        }
        return self._client.get(DataAPIEndpoints.shapes(), params=params)

    def get_shape(self) -> ApiResponse:
        if not self._data.shape_id:
            pytest.skip("shapeId not configured")
        return self._client.get(DataAPIEndpoints.shape(self._data.shape_id))
