import allure


@allure.epic("Data API")
@allure.feature("IrrigationBlocksItemGroups")
class TestIrrigationBlocksItemGroups:
    @allure.story("List ItemGroups for IrrigationBlock")
    def test_list_item_groups(self, dataapi_service):
        dataapi_service.get_irrigation_block_item_groups().assert_ok()

    @allure.story("Get ItemGroup by id for IrrigationBlock")
    def test_get_item_group_by_id(self, dataapi_service):
        dataapi_service.get_irrigation_block_item_group().assert_ok()
