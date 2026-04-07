import allure

@allure.epic("Crop Service")
@allure.feature("SoilTypes")
class TestSoilTypes:

    @allure.story("Get Soil Types")
    def test_get_soil_types(self, crop_service):
        crop_service.get_soil_types().assert_ok()

    @allure.story("Get Soil Type by ID")
    def test_get_soil_type_by_id(self, crop_service):
        crop_service.get_soil_type().assert_ok()
