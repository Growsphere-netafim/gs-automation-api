import allure


@allure.epic("Data API")
@allure.feature("Notes")
class TestNotes:
    @allure.story("Get notes by farmId")
    def test_get_notes_by_farm(self, dataapi_service):
        dataapi_service.get_notes().assert_ok()
