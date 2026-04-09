import pytest
import allure


@allure.epic("Data API")
@allure.feature("CropUnits")
class TestCropUnits:
    @allure.story("List CropUnits by farmId with pagination")
    def test_list_crop_units(self, dataapi_service):
        dataapi_service.get_crop_units().assert_ok()

    @allure.story("Get farm CropUnits")
    def test_get_farm_crop_units(self, dataapi_service):
        dataapi_service.get_farm_crop_units().assert_ok()

    @pytest.mark.flaky
    @allure.story("Get device CropUnits")
    def test_get_device_crop_units(self, dataapi_service):
        dataapi_service.get_device_crop_units().assert_ok_or_skip_404()

    @allure.story("Get CropUnit by id")
    def test_get_crop_unit_by_id(self, dataapi_service):
        dataapi_service.get_crop_unit().assert_ok()

    @allure.story("Get CropUnit Details")
    def test_get_crop_unit_details(self, dataapi_service):
        dataapi_service.get_crop_unit_details().assert_ok()

    @allure.story("Get recommendations by deviceUuid")
    def test_get_recommendations_by_device_uuid(self, dataapi_service):
        dataapi_service.get_crop_unit_recommendations().assert_ok()
