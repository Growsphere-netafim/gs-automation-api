import allure


@allure.epic("Crop Service")
@allure.feature("Seasons")
class TestSeasons:

    @allure.story("Get Seasons List")
    def test_get_seasons(self, crop_service):
        crop_service.get_seasons().assert_ok()
