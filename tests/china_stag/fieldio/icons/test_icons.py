import allure


@allure.epic("Field IO")
@allure.feature("Icons")
class TestIcons:

    @allure.story("Get Icons List")
    def test_get_icons(self, fieldio_service):
        fieldio_service.get_icons().assert_ok()
