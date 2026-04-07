import allure


@allure.epic("CS API")
@allure.feature("TechToolbox")
class TestTechToolbox:

    @allure.story("Get Dashboard Filters")
    def test_get_dashboard_filters(self, csapi_service):
        csapi_service.get_techtoolbox_dashboard_filters().assert_ok()

    @allure.story("Get Alert Count By Alert Type")
    def test_get_alert_count_by_type(self, csapi_service, dashboard_filters):
        csapi_service.get_techtoolbox_stats_alert_type(dashboard_filters).assert_ok()

    @allure.story("Get Alert Count By Device Type")
    def test_get_alert_count_by_device_type(self, csapi_service, dashboard_filters):
        csapi_service.get_techtoolbox_stats_alert_device_type(dashboard_filters).assert_ok()

    @allure.story("Get Total Alerts By Type")
    def test_get_total_alerts_by_type(self, csapi_service, dashboard_filters):
        csapi_service.get_techtoolbox_stats_total_alert_type(dashboard_filters).assert_ok()

    @allure.story("Get Alerts By Type With Icons")
    def test_get_alerts_by_type_icons(self, csapi_service, dashboard_filters):
        csapi_service.get_techtoolbox_stats_total_overall(dashboard_filters).assert_ok()

    @allure.story("Get Alerts By Distributors")
    def test_get_alerts_by_distributors(self, csapi_service, dashboard_filters):
        csapi_service.get_techtoolbox_stats_alerts_by_distributors(dashboard_filters).assert_ok()

    @allure.story("Get Alerts By Dealers")
    def test_get_alerts_by_dealers(self, csapi_service, dashboard_filters):
        csapi_service.get_techtoolbox_stats_alerts_by_dealers(dashboard_filters).assert_ok()

    @allure.story("Get Alerts By Companies")
    def test_get_alerts_by_companies(self, csapi_service, dashboard_filters):
        csapi_service.get_techtoolbox_stats_alerts_by_companies(dashboard_filters).assert_ok()

    @allure.story("Get Alerts By Farms")
    def test_get_alerts_by_farms(self, csapi_service, dashboard_filters):
        csapi_service.get_techtoolbox_stats_alerts_by_farms(dashboard_filters).assert_ok()

    @allure.story("Get Alerted Devices")
    def test_get_alerted_devices(self, csapi_service, dashboard_filters):
        csapi_service.get_techtoolbox_alerted_devices(dashboard_filters).assert_ok()
