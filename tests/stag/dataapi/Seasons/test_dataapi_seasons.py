import allure


@allure.epic("Data API")
@allure.feature("Seasons")
class TestSeasons:
    @allure.story("Get Season by id")
    def test_get_season_by_id(self, dataapi_service):
        dataapi_service.get_season().assert_ok()
