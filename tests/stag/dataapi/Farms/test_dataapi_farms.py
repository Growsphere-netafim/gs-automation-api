import allure


@allure.epic("Data API")
@allure.feature("Farms")
class TestFarms:
    @allure.story("Get farm tree")
    def test_get_farm_tree(self, dataapi_service):
        dataapi_service.get_farm_tree().assert_ok()

    @allure.story("Get farms details by ids")
    def test_get_farms_details(self, dataapi_service):
        dataapi_service.get_farms_details().assert_ok()

    @allure.story("Check farm hasValves")
    def test_get_farm_has_valves(self, dataapi_service):
        dataapi_service.get_farm_has_valves().assert_ok()
