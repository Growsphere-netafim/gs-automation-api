import allure


@allure.epic("CS API")
@allure.feature("Dealers")
class TestDealers:

    @allure.story("Get Dealers by Distributor")
    def test_get_dealers_by_distributor(self, csapi_service):
        csapi_service.get_dealers_by_distributor().assert_ok()

    @allure.story("Get All Dealers")
    def test_get_all_dealers(self, csapi_service):
        csapi_service.get_dealers().assert_ok()

    @allure.story("Get Dealers as Country Names")
    def test_get_dealers_country_names(self, csapi_service):
        csapi_service.get_country_names().assert_ok()

    @allure.story("Get Dealer by ID")
    def test_get_dealer_by_id(self, csapi_service):
        csapi_service.get_dealer().assert_ok()
