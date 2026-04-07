import allure


@allure.epic("Field IO")
@allure.feature("FieldIO - IoGroups")
class TestIoGroups:

    @allure.story("Get IO Group by ID")
    def test_get_io_group_by_id(self, fieldio_service):
        fieldio_service.get_io_group().assert_ok()

    @allure.story("List IO Groups")
    def test_get_io_groups(self, fieldio_service):
        fieldio_service.get_io_groups().assert_ok()
