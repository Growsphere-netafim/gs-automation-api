import allure


@allure.epic("Field IO")
@allure.feature("FieldIO - Thresholds")
class TestThresholds:

    @allure.story("List Thresholds")
    def test_get_thresholds(self, fieldio_service):
        fieldio_service.get_thresholds().assert_ok()
