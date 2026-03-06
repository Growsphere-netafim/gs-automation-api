class DataAPIEndpoints:
    # Farms
    @staticmethod
    def farm_tree(farm_id: str) -> str:
        return f"api/Farms/{farm_id}/tree"

    @staticmethod
    def farms_details() -> str:
        return "api/Farms/farmsDetails"

    @staticmethod
    def farm_has_valves(farm_id: str) -> str:
        return f"api/Farms/{farm_id}/hasValves"

    # Seasons
    @staticmethod
    def season(season_id) -> str:
        return f"api/Seasons/{season_id}"

    # CropAdvisor
    @staticmethod
    def crop_advisor(farm_id: str) -> str:
        return f"api/CropAdvisor/{farm_id}"

    # CropModel
    @staticmethod
    def crop_model_crop_units(farm_id: str, crop_unit_id: str) -> str:
        return f"api/CropModel/Farms/{farm_id}/CropUnits/{crop_unit_id}"

    @staticmethod
    def crop_model_response_data(farm_id: str) -> str:
        return f"api/CropModel/Farms/{farm_id}/ResponseData"

    # CropProtocols
    @staticmethod
    def crop_protocol(crop_protocol_id) -> str:
        return f"api/CropProtocols/{crop_protocol_id}"

    @staticmethod
    def crop_protocols() -> str:
        return "api/CropProtocols"

    @staticmethod
    def crop_protocols_deleted() -> str:
        return "api/CropProtocols/deleted"

    # CropUnits
    @staticmethod
    def crop_units() -> str:
        return "api/CropUnits"

    @staticmethod
    def farm_crop_units(farm_id: str) -> str:
        return f"api/farms/{farm_id}/CropUnits"

    @staticmethod
    def device_crop_units(farm_id: str, device_id: str) -> str:
        return f"api/farms/{farm_id}/devices/{device_id}/CropUnits"

    @staticmethod
    def crop_unit(crop_unit_id: str) -> str:
        return f"api/CropUnits/{crop_unit_id}"

    @staticmethod
    def crop_unit_details(crop_unit_id: str) -> str:
        return f"api/CropUnits/{crop_unit_id}/Details"

    @staticmethod
    def crop_unit_recommendations(device_uuid: str) -> str:
        return f"api/CropUnits/{device_uuid}/recommendations"

    # CropUnits ItemGroups
    @staticmethod
    def crop_unit_item_groups(crop_unit_id: str) -> str:
        return f"api/CropUnits/{crop_unit_id}/ItemGroups"

    @staticmethod
    def crop_unit_item_group(crop_unit_id: str, item_group_id: str) -> str:
        return f"api/CropUnits/{crop_unit_id}/ItemGroups/{item_group_id}"

    # CropUnits Items
    @staticmethod
    def crop_unit_items(crop_unit_id: str, item_group_id: str) -> str:
        return f"api/CropUnits/{crop_unit_id}/ItemGroups/{item_group_id}/Items"

    @staticmethod
    def crop_unit_item(crop_unit_id: str, item_group_id: str, item_id: str) -> str:
        return f"api/CropUnits/{crop_unit_id}/ItemGroups/{item_group_id}/Items/{item_id}"

    # Farms ItemGroups
    @staticmethod
    def farm_item_groups(farm_id: str) -> str:
        return f"api/Farms/{farm_id}/ItemGroups"

    @staticmethod
    def farm_item_group(farm_id: str, item_group_id: str) -> str:
        return f"api/Farms/{farm_id}/ItemGroups/{item_group_id}"

    # Farms Items
    @staticmethod
    def farm_items(farm_id: str, item_group_id: str) -> str:
        return f"api/Farms/{farm_id}/ItemGroups/{item_group_id}/Items"

    @staticmethod
    def farm_item(farm_id: str, item_group_id: str, item_id: str) -> str:
        return f"api/Farms/{farm_id}/ItemGroups/{item_group_id}/Items/{item_id}"

    # Geolocation
    @staticmethod
    def geolocation(irrigation_block_id: str) -> str:
        return f"api/Geolocation/{irrigation_block_id}"

    # IrrigationBlocks
    @staticmethod
    def irrigation_block(irrigation_block_id: str) -> str:
        return f"api/IrrigationBlocks/{irrigation_block_id}"

    @staticmethod
    def irrigation_blocks() -> str:
        return "api/IrrigationBlocks"

    @staticmethod
    def irrigation_blocks_unconnected(farm_id: str) -> str:
        return f"api/IrrigationBlocks/unconnected/{farm_id}"

    # IrrigationBlocks ItemGroups
    @staticmethod
    def irrigation_block_item_groups(irrigation_block_id: str) -> str:
        return f"api/IrrigationBlocks/{irrigation_block_id}/ItemGroups"

    @staticmethod
    def irrigation_block_item_group(irrigation_block_id: str, item_group_id: str) -> str:
        return f"api/IrrigationBlocks/{irrigation_block_id}/ItemGroups/{item_group_id}"

    # IrrigationBlocks Items
    @staticmethod
    def irrigation_block_items(irrigation_block_id: str, item_group_id: str) -> str:
        return f"api/IrrigationBlocks/{irrigation_block_id}/ItemGroups/{item_group_id}/Items"

    @staticmethod
    def irrigation_block_item(irrigation_block_id: str, item_group_id: str, item_id: str) -> str:
        return f"api/IrrigationBlocks/{irrigation_block_id}/ItemGroups/{item_group_id}/Items/{item_id}"

    # IrrigationModel
    @staticmethod
    def irrigation_model_response_data(farm_id: str, date: str) -> str:
        return f"api/IrrigationModel/ResponseData/{farm_id}/{date}"

    @staticmethod
    def irrigation_model_response_ui_data(farm_id: str, crop_unit_id: str) -> str:
        return f"api/IrrigationModel/Farms/{farm_id}/CropUnits/{crop_unit_id}/ResponseUIData"

    @staticmethod
    def irrigation_model_crop_unit_response_data(farm_id: str, crop_unit_id: str) -> str:
        return f"api/IrrigationModel/Farms/{farm_id}/CropUnits/{crop_unit_id}/ResponseData"

    # Items
    @staticmethod
    def item(item_id: str) -> str:
        return f"api/Items/{item_id}"

    # Notes
    @staticmethod
    def notes(farm_id: str) -> str:
        return f"api/{farm_id}/notes"

    # SeasonChanges
    @staticmethod
    def season_changes(season_id) -> str:
        return f"api/seasons/{season_id}/seasonChanges"

    # SeasonProperties
    @staticmethod
    def season_properties(farm_id: str, season_id) -> str:
        return f"api/farms/{farm_id}/Seasons/{season_id}/SeasonProperties"

    # Shapes
    @staticmethod
    def shapes() -> str:
        return "api/Shapes"

    @staticmethod
    def shape(shape_id: str) -> str:
        return f"api/Shapes/{shape_id}"
