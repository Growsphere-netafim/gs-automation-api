import allure


@allure.epic("CS API")
@allure.feature("General")
class TestGeneral:

    @allure.story("Base Health Check")
    def test_base_health_check(self, csapi_service):
        csapi_service.get_root().assert_ok()

    @allure.story("Get Devices (OData)")
    def test_get_devices_odata(self, csapi_service):
        csapi_service.get_devices_odata().assert_ok()

    @allure.story("Get Device Events")
    def test_get_device_events(self, csapi_service):
        csapi_service.get_device_events().assert_ok()

    @allure.story("Get Metadata")
    def test_get_metadata(self, csapi_service):
        csapi_service.get_metadata().assert_ok()

    @allure.story("Get Service Document")
    def test_get_service_document(self, csapi_service):
        csapi_service.get_service_document().assert_ok()
