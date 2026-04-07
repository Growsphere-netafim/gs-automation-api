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
        csapi_service.get_cultures().assert_ok()
