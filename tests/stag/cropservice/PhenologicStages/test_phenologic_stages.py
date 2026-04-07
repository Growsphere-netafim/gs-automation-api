import allure

@allure.epic("Crop Service")
@allure.feature("PhenologicStages")
class TestPhenologicStages:

    @allure.story("Get Phenologic Stages")
    def test_get_phenologic_stages(self, crop_service):
        crop_service.get_phenologic_stages().assert_ok()

    @allure.story("Get Phenologic Stage by ID")
    def test_get_phenologic_stage_by_id(self, crop_service):
        crop_service.get_phenologic_stage().assert_ok()
