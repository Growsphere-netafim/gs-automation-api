import allure


@allure.epic("Field IO")
@allure.feature("FieldIO - Remotes")
class TestRemotes:

    @allure.story("List Remotes")
    def test_get_remotes(self, fieldio_service):
        resp = fieldio_service.get_remotes()
        resp.assert_ok()

    @allure.story("Get Remote by ID")
    def test_get_remote_by_id(self, fieldio_service):
        resp = fieldio_service.get_remote()
        resp.assert_ok()
