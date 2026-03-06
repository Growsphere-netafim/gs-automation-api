import allure


@allure.epic("Data API")
@allure.feature("IrrigationBlocks")
class TestIrrigationBlocks:
    @allure.story("Get IrrigationBlock by id")
    def test_get_irrigation_block_by_id(self, dataapi_service):
        resp = dataapi_service.get_irrigation_block()
        resp.assert_ok()

    @allure.story("List IrrigationBlocks by farmId")
    def test_list_irrigation_blocks(self, dataapi_service):
        resp = dataapi_service.get_irrigation_blocks()
        resp.assert_ok()

    @allure.story("List unconnected IrrigationBlocks by farmId")
    def test_list_unconnected_irrigation_blocks(self, dataapi_service):
        resp = dataapi_service.get_irrigation_blocks_unconnected()
        resp.assert_ok()
