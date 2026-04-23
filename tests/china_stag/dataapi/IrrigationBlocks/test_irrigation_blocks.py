import allure
import pytest


@allure.epic("Data API")
@allure.feature("IrrigationBlocks")
class TestIrrigationBlocks:

    @allure.story("Get IrrigationBlocks List")
    def test_get_irrigation_blocks(self, dataapi_service):
        dataapi_service.get_irrigation_blocks().assert_ok()

    @pytest.mark.flaky
    @allure.story("Get IrrigationBlock by ID")
    def test_get_irrigation_block_by_id(self, dataapi_service):
        dataapi_service.get_irrigation_block().assert_ok_or_skip_404("IrrigationBlock not found in china prod")
