import allure
import pytest


@allure.epic("CS API")
@allure.feature("Enterprises")
class TestEnterprises:

    @allure.story("Get Enterprises")
    def test_get_enterprises(self, csapi_service):
        csapi_service.get_enterprises().assert_ok()

    @allure.story("Get Enterprise Details")
    def test_get_enterprise_details(self, csapi_service):
        csapi_service.get_enterprise().assert_ok()

    @allure.story("Get Enterprise Identifiers")
    def test_get_enterprise_ids(self, csapi_service):
        csapi_service.get_enterprise_ids().assert_ok()

    @allure.story("Check Name Availability")
    def test_check_name_availability(self, csapi_service):
        csapi_service.get_enterprise_name_availability().assert_ok()

    @allure.story("Get Enterprise Farms")
    def test_get_enterprise_farms(self, csapi_service):
        csapi_service.get_enterprise_farms().assert_ok()

    @allure.story("Get Enterprise Users Details")
    def test_get_enterprise_users_details(self, csapi_service):
        csapi_service.get_enterprise_users_details().assert_ok()

    @pytest.mark.flaky
    # TODO: enterprise hierarchy returns 404 in QA1 for the configured enterpriseId.
    # To fix: find an enterpriseId that has hierarchy data configured.
    @allure.story("Get Hierarchy Items")
    def test_get_hierarchy_items(self, csapi_service):
        csapi_service.get_enterprise_hierarchy().assert_ok_or_skip_404("Enterprise hierarchy not found")
        csapi_service.get_dealer_hierarchy().assert_ok()
        csapi_service.get_distributor_hierarchy().assert_ok()
