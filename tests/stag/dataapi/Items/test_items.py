import allure
import pytest


@allure.epic("Data API")
@allure.feature("Items")
class TestItems:
    @pytest.mark.flaky
    @allure.story("Get Item by itemId")
    def test_get_item_by_id(self, dataapi_service):
        dataapi_service.get_item().assert_ok()
