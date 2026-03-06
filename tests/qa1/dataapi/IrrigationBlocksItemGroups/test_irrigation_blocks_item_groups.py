import allure


@allure.epic("Data API")
@allure.feature("IrrigationBlocksItemGroups")
class TestIrrigationBlocksItemGroups:
    @allure.story("List ItemGroups for IrrigationBlock")
    def test_list_item_groups(self, dataapi_service):
        resp = dataapi_service.get_irrigation_block_item_groups()
        resp.assert_ok()

    @allure.story("Get ItemGroup by id for IrrigationBlock")
    def test_get_item_group_by_id(self, dataapi_service):
        resp = dataapi_service.get_irrigation_block_item_group()
        resp.assert_ok()
