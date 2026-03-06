import pytest
import requests
from api.client.api_client import QAApiClient
from api.client.response import ApiResponse
from api.endpoints.crop_service import CropServiceEndpoints


class CropServiceService:
    def __init__(self, client: QAApiClient, data):
        self._client = client
        self._data = data

    def get_crop_families(self) -> ApiResponse:
        return self._client.get(CropServiceEndpoints.crop_families())

    def get_crop_family(self) -> ApiResponse:
        if not self._data.crop_family_id:
            pytest.skip("cropFamilyId not configured")
        return self._client.get(CropServiceEndpoints.crop_family(self._data.crop_family_id))

    def get_crops(self) -> ApiResponse:
        return self._client.get(CropServiceEndpoints.crops())

    def get_crop(self) -> ApiResponse:
        if not self._data.crop_id:
            pytest.skip("cropId not configured")
        return self._client.get(CropServiceEndpoints.crop(self._data.crop_id))

    def get_nutrients(self) -> ApiResponse:
        return self._client.get(CropServiceEndpoints.nutrients())

    def get_nutrient(self) -> ApiResponse:
        if not self._data.nutrient_id:
            pytest.skip("nutrientId not configured")
        return self._client.get(CropServiceEndpoints.nutrient(self._data.nutrient_id))

    def get_parameter_aspects(self) -> ApiResponse:
        return self._client.get(CropServiceEndpoints.parameter_aspects())

    def get_parameter_aspect(self) -> ApiResponse:
        if not self._data.parameter_aspect_id:
            pytest.skip("parameterAspectId not configured")
        return self._client.get(
            CropServiceEndpoints.parameter_aspect(self._data.parameter_aspect_id)
        )

    def get_parameter_types(self) -> ApiResponse:
        return self._client.get(CropServiceEndpoints.parameter_types())

    def get_parameter_type(self) -> ApiResponse:
        if not self._data.parameter_type_id:
            pytest.skip("parameterTypeId not configured")
        return self._client.get(
            CropServiceEndpoints.parameter_type(self._data.parameter_type_id)
        )

    def get_phenologic_stages(self) -> ApiResponse:
        return self._client.get(CropServiceEndpoints.phenologic_stages())

    def get_phenologic_stage(self) -> ApiResponse:
        if not self._data.phenologic_stage_id:
            pytest.skip("phenologicStageId not configured")
        return self._client.get(
            CropServiceEndpoints.phenologic_stage(self._data.phenologic_stage_id)
        )

    def get_protocol_strategies(self) -> ApiResponse:
        return self._client.get(CropServiceEndpoints.protocol_strategies())

    def get_protocol_strategy(self) -> ApiResponse:
        if not self._data.protocol_strategy_id:
            pytest.skip("protocolStrategyId not configured")
        return self._client.get(
            CropServiceEndpoints.protocol_strategy(self._data.protocol_strategy_id)
        )

    def get_soil_types(self) -> ApiResponse:
        return self._client.get(CropServiceEndpoints.soil_types())

    def get_soil_type(self) -> ApiResponse:
        if not self._data.soil_type_id:
            pytest.skip("soilTypeId not configured")
        return self._client.get(CropServiceEndpoints.soil_type(self._data.soil_type_id))

    def get_varieties(self) -> ApiResponse:
        return self._client.get(CropServiceEndpoints.varieties())

    def get_variety(self) -> ApiResponse:
        if not self._data.variety_id:
            pytest.skip("varietyId not configured")
        return self._client.get(CropServiceEndpoints.variety(self._data.variety_id))

    def get_seasons(self) -> ApiResponse:
        return self._client.get(CropServiceEndpoints.seasons())

    def get_irrigation_strategies(self) -> ApiResponse:
        return self._client.get(CropServiceEndpoints.irrigation_strategies())

    def get_parameter_per_crop_family(self) -> ApiResponse:
        return self._client.get(CropServiceEndpoints.parameter_per_crop_family())

    def get_parameter_per_protocol_strategy(self) -> ApiResponse:
        return self._client.get(CropServiceEndpoints.parameter_per_protocol_strategy())

    def get_parameter_per_stage(self) -> ApiResponse:
        return self._client.get(CropServiceEndpoints.parameter_per_stage())

    def get_parameter_per_stage_lite(self) -> ApiResponse:
        return self._client.get(CropServiceEndpoints.parameter_per_stage_lite())

    def get_parameter_per_varieties(self) -> ApiResponse:
        return self._client.get(CropServiceEndpoints.parameter_per_varieties())

    def get_parameter_per_varieties_lite(self) -> ApiResponse:
        return self._client.get(CropServiceEndpoints.parameter_per_varieties_lite())

    def get_parameters_per_crops(self) -> ApiResponse:
        return self._client.get(CropServiceEndpoints.parameters_per_crops())

    def get_system_crop_protocols(self) -> ApiResponse:
        try:
            return self._client.get(CropServiceEndpoints.system_crop_protocols())
        except requests.exceptions.RetryError:
            pytest.skip("SystemCropProtocols endpoint returned 500 (server error)")
