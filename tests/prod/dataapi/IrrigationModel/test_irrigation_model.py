import allure
import pytest


@allure.epic("Data API")
@allure.feature("IrrigationModel")
class TestIrrigationModel:
    @pytest.mark.flaky
    @allure.story("Get IrrigationModel ResponseData by farmId and date")
    def test_get_response_data_by_date(self, dataapi_service):
        dataapi_service.get_irrigation_model_response_data().assert_ok_or_skip_404("IrrigationModel not found in prod")
