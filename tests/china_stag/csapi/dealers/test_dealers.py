import allure


@allure.epic("CS API")
@allure.feature("Dealers")
class TestDealers:

    @allure.story("Get All Dealers")
    def test_get_all_dealers(self, csapi_service):
        csapi_service.get_dealers().assert_ok()

    @allure.story("Get Dealers as Country Names")
    def test_get_dealers_country_names(self, csapi_service):
        csapi_service.get_country_names().assert_ok()
