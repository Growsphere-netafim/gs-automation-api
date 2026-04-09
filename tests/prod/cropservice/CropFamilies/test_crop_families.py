import allure

@allure.epic("Crop Service")
@allure.feature("CropFamilies")
class TestCropFamilies:

    @allure.story("Get Crop Families List")
    def test_get_crop_families(self, crop_service):
        crop_service.get_crop_families().assert_ok()

    @allure.story("Get Crop Family by ID")
    def test_get_crop_family_by_id(self, crop_service):
        crop_service.get_crop_family().assert_ok()
