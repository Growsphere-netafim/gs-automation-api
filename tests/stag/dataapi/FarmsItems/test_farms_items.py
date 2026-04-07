import allure
import pytest


@allure.epic("Data API")
@allure.feature("FarmsItems")
class TestFarmsItems:
    @allure.story("List Items for ItemGroup in farm")
    def test_list_items(self, dataapi_service):
        dataapi_service.get_farm_items().assert_ok()

    @pytest.mark.flaky
    @allure.story("Get Item by id in ItemGroup for farm")
    def test_get_item_by_id(self, dataapi_service):
        dataapi_service.get_farm_item().assert_ok()
