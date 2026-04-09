import allure


@allure.epic("Field IO")
@allure.feature("FieldIO - Remotes")
class TestRemotes:

    @allure.story("List Remotes")
    def test_get_remotes(self, fieldio_service):
        fieldio_service.get_remotes().assert_ok()

    @allure.story("Get Remote by ID")
    def test_get_remote_by_id(self, fieldio_service):
        fieldio_service.get_remote().assert_ok()
