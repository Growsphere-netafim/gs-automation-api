import allure


@allure.epic("Field IO")
@allure.feature("FieldIO - Icons")
class TestIcons:

    @allure.story("List Icons")
    def test_get_icons(self, fieldio_service):
        resp = fieldio_service.get_icons()
        resp.assert_ok()
