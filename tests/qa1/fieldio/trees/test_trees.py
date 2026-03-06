import allure


@allure.epic("Field IO")
@allure.feature("FieldIO - Trees")
class TestTrees:

    @allure.story("Get Base Tree")
    def test_get_base_tree(self, fieldio_service):
        resp = fieldio_service.get_base_tree()
        resp.assert_ok()

    @allure.story("Get Device Tree")
    def test_get_device_tree(self, fieldio_service):
        resp = fieldio_service.get_device_tree()
        resp.assert_ok()

    @allure.story("Get Farm Trees")
    def test_get_trees(self, fieldio_service):
        resp = fieldio_service.get_farm_trees()
        resp.assert_ok()

    @allure.story("Get Device Tree Lite")
    def test_get_device_tree_lite(self, fieldio_service):
        resp = fieldio_service.get_device_tree_lite()
        resp.assert_ok()
