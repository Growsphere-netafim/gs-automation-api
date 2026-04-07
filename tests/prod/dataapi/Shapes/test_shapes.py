import allure
import pytest


@allure.epic("Data API")
@allure.feature("Shapes")
class TestShapes:
    @pytest.mark.flaky
    @allure.story("Get Shape by id")
    def test_get_shape_by_id(self, dataapi_service):
        dataapi_service.get_shape().assert_ok_or_skip_404("Shape not found in prod")
