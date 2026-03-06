import allure

@allure.epic("Crop Service")
@allure.feature("Crops")
class TestCrops:

    @allure.story("Get Crops List")
    def test_get_crops(self, crop_service):
        resp = crop_service.get_crops()
        resp.assert_ok()

    @allure.story("Get Crop by ID")
    def test_get_crop_by_id(self, crop_service):
        resp = crop_service.get_crop()
        resp.assert_ok()
