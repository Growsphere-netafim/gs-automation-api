import allure


@allure.epic("Field IO")
@allure.feature("FieldIO - Icons")
class TestIcons:

    @allure.story("List Icons")
    def test_get_icons(self, fieldio_service):
        fieldio_service.get_icons().assert_ok()
