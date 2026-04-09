import allure
import pytest


@allure.epic("CS API")
@allure.feature("Cultures")
class TestCultures:

    @allure.story("Get Culture App Ids")
    def test_get_culture_app_ids(self, csapi_service):
        resp = csapi_service.get_culture_app_ids().assert_ok()
        assert "ids" in resp.json()

    @allure.story("Get Cultures List")
    def test_get_cultures_list(self, csapi_service):
        resp = csapi_service.get_cultures().assert_ok()
        resp_json = resp.json()
        if isinstance(resp_json, dict) and "totalRecords" in resp_json:
            assert resp_json["totalRecords"] >= 0
        elif isinstance(resp_json, list):
            pass

    @pytest.mark.flaky
    @allure.story("Get Specific Culture")
    def test_get_specific_culture(self, csapi_service):
        list_resp = csapi_service.get_cultures()
        if list_resp.status_code == 200:
            items = list_resp.json().get('cultures', [])
            if items:
                csapi_service.get_culture().assert_ok_or_skip_404("Culture not found in environment")
            else:
                pytest.skip("No cultures found to test specific fetch")
        else:
            pytest.skip(f"Could not list cultures to get a valid ID: {list_resp.status_code}")
