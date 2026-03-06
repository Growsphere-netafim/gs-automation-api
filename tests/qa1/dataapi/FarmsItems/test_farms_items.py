import allure
import pytest


@allure.epic("Data API")
@allure.feature("FarmsItems")
class TestFarmsItems:
    @allure.story("List Items for ItemGroup in farm")
    def test_list_items(self, dataapi_service):
        resp = dataapi_service.get_farm_items()
        resp.assert_ok()

    @pytest.mark.flaky
    # TODO: no farm in QA1 (from token list) has Items inside its ItemGroups.
    # To fix: find a farmId where GET /api/Farms/{id}/ItemGroups/{groupId}/Items returns non-empty list
    @allure.story("Get Item by id in ItemGroup for farm")
    def test_get_item_by_id(self, dataapi_service):
        resp = dataapi_service.get_farm_item()
        resp.assert_ok()
