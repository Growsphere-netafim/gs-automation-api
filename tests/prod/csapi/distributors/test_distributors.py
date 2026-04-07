import allure


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
