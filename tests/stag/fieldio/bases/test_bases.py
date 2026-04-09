import allure


@allure.epic("Field IO")
@allure.feature("FieldIO - Bases")
class TestBases:

    @allure.story("List Bases")
    def test_get_bases(self, fieldio_service):
        fieldio_service.get_bases().assert_ok()

    @allure.story("Get Bases Address")
    def test_get_bases_address(self, fieldio_service):
        fieldio_service.get_bases_address().assert_ok()

    @allure.story("Get Base by ID")
    def test_get_base_by_id(self, fieldio_service):
        fieldio_service.get_base().assert_ok()

    @allure.story("Get Base Address by ID")
    def test_get_base_address_by_id(self, fieldio_service):
        fieldio_service.get_base_address().assert_ok()

    @allure.story("Get Bases by System Type")
    def test_get_bases_by_system_type(self, fieldio_service):
        fieldio_service.get_bases_by_system_type().assert_ok()
