import allure


@allure.epic("Data API")
@allure.feature("Shapes")
class TestShapes:
    @allure.story("List Shapes by farmId with pagination")
    def test_list_shapes(self, dataapi_service):
        resp = dataapi_service.get_shapes()
        resp.assert_ok()

    @allure.story("Get Shape by id")
    def test_get_shape_by_id(self, dataapi_service):
        resp = dataapi_service.get_shape()
        resp.assert_ok()
