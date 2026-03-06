import allure

@allure.epic("Crop Service")
@allure.feature("ParameterTypes")
class TestParameterTypes:

    @allure.story("Get Parameter Types")
    def test_get_parameter_types(self, crop_service):
        resp = crop_service.get_parameter_types()
        resp.assert_ok()

    @allure.story("Get Parameter Type by ID")
    def test_get_parameter_type_by_id(self, crop_service):
        resp = crop_service.get_parameter_type()
        resp.assert_ok()
