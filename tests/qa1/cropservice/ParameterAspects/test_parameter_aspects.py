import allure

@allure.epic("Crop Service")
@allure.feature("ParameterAspects")
class TestParameterAspects:

    @allure.story("Get Parameter Aspects")
    def test_get_parameter_aspects(self, crop_service):
        resp = crop_service.get_parameter_aspects()
        resp.assert_ok()

    @allure.story("Get Parameter Aspect by ID")
    def test_get_parameter_aspect_by_id(self, crop_service):
        resp = crop_service.get_parameter_aspect()
        resp.assert_ok()
