import allure


@allure.epic("Field IO")
@allure.feature("FieldIO - Trees")
class TestTrees:

    @allure.story("Get Base Tree")
    def test_get_base_tree(self, fieldio_service):
        fieldio_service.get_base_tree().assert_ok()

    @allure.story("Get Device Tree")
    def test_get_device_tree(self, fieldio_service):
        fieldio_service.get_device_tree().assert_ok()

    @allure.story("Get Farm Trees")
    def test_get_trees(self, fieldio_service):
        fieldio_service.get_farm_trees().assert_ok()

    @allure.story("Get Device Tree Lite")
    def test_get_device_tree_lite(self, fieldio_service):
        fieldio_service.get_device_tree_lite().assert_ok()
