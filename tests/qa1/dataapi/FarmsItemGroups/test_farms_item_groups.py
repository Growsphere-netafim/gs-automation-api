import allure


@allure.epic("Data API")
@allure.feature("FarmsItemGroups")
class TestFarmsItemGroups:
    @allure.story("List ItemGroups for farm")
    def test_list_farm_item_groups(self, dataapi_service):
        resp = dataapi_service.get_farm_item_groups()
        resp.assert_ok()

    @allure.story("Get ItemGroup by id for farm")
    def test_get_farm_item_group_by_id(self, dataapi_service):
        resp = dataapi_service.get_farm_item_group()
        resp.assert_ok()
