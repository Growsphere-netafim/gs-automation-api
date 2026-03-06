import allure

@allure.epic("Crop Service")
@allure.feature("PhenologicStages")
class TestPhenologicStages:

    @allure.story("Get Phenologic Stages")
    def test_get_phenologic_stages(self, crop_service):
        resp = crop_service.get_phenologic_stages()
        resp.assert_ok()

    @allure.story("Get Phenologic Stage by ID")
    def test_get_phenologic_stage_by_id(self, crop_service):
        resp = crop_service.get_phenologic_stage()
        resp.assert_ok()
