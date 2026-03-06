import allure

@allure.epic("Crop Service")
@allure.feature("Seasons")
class TestSeasons:

    @allure.story("Get Seasons")
    def test_get_seasons(self, crop_service):
        resp = crop_service.get_seasons()
        resp.assert_ok()
