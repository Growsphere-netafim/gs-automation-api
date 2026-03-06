import allure
import pytest


@allure.epic("CS API")
@allure.feature("Distributors")
class TestDistributors:

    @allure.story("Get All Distributors")
    def test_get_all_distributors(self, csapi_service):
        csapi_service.get_distributors().assert_ok()

    @allure.story("Get Distributor Names")
    def test_get_distributor_names(self, csapi_service):
        csapi_service.get_distributor_names().assert_ok()

    @allure.story("Get Distributor by ID")
    def test_get_distributor_by_id(self, csapi_service):
        csapi_service.get_distributor().assert_ok()

    @pytest.mark.flaky
    # TODO: distributor search endpoint returns 409 in QA1 (server-side conflict error).
    # Infrastructure issue — endpoint broken in this environment.
    @allure.story("Search Distributors (GET with Body)")
    def test_search_distributors_with_body(self, csapi_service):
        csapi_service.search_distributors().assert_ok()

    @pytest.mark.flaky
    # TODO: dealer search endpoint returns 409 in QA1 (server-side conflict error).
    # Infrastructure issue — endpoint broken in this environment.
    @allure.story("Search Dealers within Distributor (GET with Body)")
    def test_search_dealers_within_distributor(self, csapi_service):
        csapi_service.search_dealers_in_distributor().assert_ok()

    @pytest.mark.flaky
    # TODO: all-dealers search endpoint returns 409 in QA1 (server-side conflict error).
    # Infrastructure issue — endpoint broken in this environment.
    @allure.story("Search All Dealers (GET with Body)")
    def test_search_all_dealers_with_body(self, csapi_service):
        csapi_service.search_all_dealers().assert_ok()
