import allure
import pytest


@allure.epic("Data API")
@allure.feature("IrrigationBlocksItems")
class TestIrrigationBlocksItems:
    @pytest.mark.flaky
    @allure.story("List Items for ItemGroup in IrrigationBlock")
    def test_list_items(self, dataapi_service):
        dataapi_service.get_irrigation_block_items().assert_ok_or_skip_404("IrrigationBlock not found in prod")
