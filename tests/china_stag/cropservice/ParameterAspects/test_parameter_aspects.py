import allure


@allure.epic("Crop Service")
@allure.feature("Parameter Aspects")
class TestParameterAspects:

    @allure.story("Get Parameter Aspects List")
    def test_get_parameter_aspects(self, crop_service):
        crop_service.get_parameter_aspects().assert_ok()

    @allure.story("Get Parameter Aspect by ID")
    def test_get_parameter_aspect_by_id(self, crop_service):
        crop_service.get_parameter_aspect().assert_ok()
