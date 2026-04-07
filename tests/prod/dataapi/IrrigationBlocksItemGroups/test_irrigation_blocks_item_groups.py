import allure
import pytest


@allure.epic("Data API")
@allure.feature("IrrigationBlocksItemGroups")
class TestIrrigationBlocksItemGroups:
    @pytest.mark.flaky
    @allure.story("List ItemGroups for IrrigationBlock")
    def test_list_item_groups(self, dataapi_service):
        dataapi_service.get_irrigation_block_item_groups().assert_ok_or_skip_404("IrrigationBlock not found in prod")
