import allure

@allure.epic("Crop Service")
@allure.feature("Varieties")
class TestVarieties:

    @allure.story("Get Varieties")
    def test_get_varieties(self, crop_service):
        resp = crop_service.get_varieties()
        resp.assert_ok()

    @allure.story("Get Variety by ID")
    def test_get_variety_by_id(self, crop_service):
        resp = crop_service.get_variety()
        resp.assert_ok()
