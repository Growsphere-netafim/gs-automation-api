import allure
import pytest


@allure.epic("Data API")
@allure.feature("IrrigationModel")
class TestIrrigationModel:
    @allure.story("Get IrrigationModel ResponseData by farmId and date")
    def test_get_response_data_by_date(self, dataapi_service):
        resp = dataapi_service.get_irrigation_model_response_data()
        resp.assert_ok()

    @pytest.mark.flaky
    # TODO: no CropUnit across known QA1 farms has IrrigationModel data (all return 400).
    # To fix: find a farmId + cropUnitId where IrrigationModel is configured and active
    @allure.story("Get IrrigationModel ResponseUIData")
    def test_get_response_ui_data(self, dataapi_service):
        resp = dataapi_service.get_irrigation_model_response_ui_data()
        resp.assert_any_of(200, 204)

    @pytest.mark.flaky
    # TODO: same as above — needs a cropUnitId with active IrrigationModel
    @allure.story("Get IrrigationModel ResponseData for CropUnit")
    def test_get_response_data_for_crop_unit(self, dataapi_service):
        resp = dataapi_service.get_irrigation_model_crop_unit_response_data()
        resp.assert_any_of(200, 204)
