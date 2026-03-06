import allure


@allure.epic("Data API")
@allure.feature("IrrigationBlocksItems")
class TestIrrigationBlocksItems:
    @allure.story("List Items for ItemGroup in IrrigationBlock")
    def test_list_items(self, dataapi_service):
        resp = dataapi_service.get_irrigation_block_items()
        resp.assert_ok()

    @allure.story("Get Item by id in ItemGroup for IrrigationBlock")
    def test_get_item_by_id(self, dataapi_service):
        resp = dataapi_service.get_irrigation_block_item()
        resp.assert_ok()
