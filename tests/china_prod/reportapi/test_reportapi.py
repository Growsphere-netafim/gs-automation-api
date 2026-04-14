import allure
import pytest


@allure.epic("Report API")
@allure.feature("Configuration Controller")
class TestConfiguration:

    @pytest.mark.flaky
    @allure.story("Get Configuration by User ID")
    def test_get_configuration_by_user_id(self, reportapi_service):
        reportapi_service.get_configuration().assert_ok()
