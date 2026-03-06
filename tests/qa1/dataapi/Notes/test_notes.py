import allure


@allure.epic("Data API")
@allure.feature("Notes")
class TestNotes:
    @allure.story("Get notes by farmId")
    def test_get_notes_by_farm(self, dataapi_service):
        resp = dataapi_service.get_notes()
        resp.assert_ok()
