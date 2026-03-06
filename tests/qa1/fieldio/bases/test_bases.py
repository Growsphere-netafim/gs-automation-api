import allure


@allure.epic("Field IO")
@allure.feature("FieldIO - Bases")
class TestBases:

    @allure.story("List Bases")
    def test_get_bases(self, fieldio_service):
        resp = fieldio_service.get_bases()
        resp.assert_ok()

    @allure.story("Get Bases Address")
    def test_get_bases_address(self, fieldio_service):
        resp = fieldio_service.get_bases_address()
        resp.assert_ok()

    @allure.story("Get Base by ID")
    def test_get_base_by_id(self, fieldio_service):
        resp = fieldio_service.get_base()
        resp.assert_ok()

    @allure.story("Get Base Address by ID")
    def test_get_base_address_by_id(self, fieldio_service):
        resp = fieldio_service.get_base_address()
        resp.assert_ok()

    @allure.story("Get Bases by System Type")
    def test_get_bases_by_system_type(self, fieldio_service):
        resp = fieldio_service.get_bases_by_system_type()
        resp.assert_ok()
