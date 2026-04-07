import allure
import pytest


@allure.epic("Data API")
@allure.feature("IrrigationBlocks")
class TestIrrigationBlocks:
    @pytest.mark.flaky
    @allure.story("Get IrrigationBlock by id")
    def test_get_irrigation_block_by_id(self, dataapi_service):
        dataapi_service.get_irrigation_block().assert_ok_or_skip_404("IrrigationBlock not found in prod")
