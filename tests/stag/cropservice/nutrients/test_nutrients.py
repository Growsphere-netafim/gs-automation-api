import allure

@allure.epic("Crop Service")
@allure.feature("Nutrients")
class TestNutrients:

    @allure.story("Get Nutrients")
    def test_get_nutrients(self, crop_service):
        crop_service.get_nutrients().assert_ok()

    @allure.story("Get Nutrient by ID")
    def test_get_nutrient_by_id(self, crop_service):
        crop_service.get_nutrient().assert_ok()
