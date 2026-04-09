import allure
import pytest


@allure.epic("Data API")
@allure.feature("IrrigationModel")
class TestIrrigationModel:
    @allure.story("Get IrrigationModel ResponseData by farmId and date")
    def test_get_response_data_by_date(self, dataapi_service):
        dataapi_service.get_irrigation_model_response_data().assert_ok()

    @pytest.mark.flaky
    @allure.story("Get IrrigationModel ResponseUIData")
    def test_get_response_ui_data(self, dataapi_service):
        dataapi_service.get_irrigation_model_response_ui_data().assert_any_of(200, 204)

    @pytest.mark.flaky
    @allure.story("Get IrrigationModel ResponseData for CropUnit")
    def test_get_response_data_for_crop_unit(self, dataapi_service):
        dataapi_service.get_irrigation_model_crop_unit_response_data().assert_any_of(200, 204)
