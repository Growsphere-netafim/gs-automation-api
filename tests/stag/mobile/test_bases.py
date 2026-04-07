import allure


@allure.epic("Mobile BFF")
@allure.feature("Bases Controller")
class TestMobileBases:

    @allure.story("Get Base Topology")
    def test_get_base_topology(self, mobile_service):
        mobile_service.get_base_topology().assert_ok()

    @allure.story("Get Base Tree")
    def test_get_base_tree(self, mobile_service):
        mobile_service.get_base_tree().assert_ok()
