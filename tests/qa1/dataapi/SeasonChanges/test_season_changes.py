import allure


@allure.epic("Data API")
@allure.feature("SeasonChanges")
class TestSeasonChanges:
    @allure.story("Get SeasonChanges by seasonId with parameters")
    def test_get_season_changes(self, dataapi_service):
        resp = dataapi_service.get_season_changes()
        resp.assert_ok()
