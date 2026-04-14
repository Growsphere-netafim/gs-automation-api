import allure


@allure.epic("Data API")
@allure.feature("Shapes")
class TestShapes:

    @allure.story("Get Shapes List")
    def test_get_shapes(self, dataapi_service):
        dataapi_service.get_shapes().assert_ok()
