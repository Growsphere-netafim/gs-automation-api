class CropServiceEndpoints:
    @staticmethod
    def crop_families() -> str:
        return "api/CropFamilies"

    @staticmethod
    def crop_family(crop_family_id) -> str:
        return f"api/CropFamilies/{crop_family_id}"

    @staticmethod
    def crops() -> str:
        return "api/Crops"

    @staticmethod
    def crop(crop_id) -> str:
        return f"api/Crops/{crop_id}"

    @staticmethod
    def nutrients() -> str:
        return "api/Nutrients"

    @staticmethod
    def nutrient(nutrient_id) -> str:
        return f"api/Nutrients/{nutrient_id}"

    @staticmethod
    def parameter_aspects() -> str:
        return "api/ParameterAspects"

    @staticmethod
    def parameter_aspect(parameter_aspect_id) -> str:
        return f"api/ParameterAspects/{parameter_aspect_id}"

    @staticmethod
    def parameter_types() -> str:
        return "api/ParameterTypes"

    @staticmethod
    def parameter_type(parameter_type_id) -> str:
        return f"api/ParameterTypes/{parameter_type_id}"

    @staticmethod
    def phenologic_stages() -> str:
        return "api/PhenologicStages"

    @staticmethod
    def phenologic_stage(phenologic_stage_id) -> str:
        return f"api/PhenologicStages/{phenologic_stage_id}"

    @staticmethod
    def protocol_strategies() -> str:
        return "api/ProtocolStrategies"

    @staticmethod
    def protocol_strategy(protocol_strategy_id) -> str:
        return f"api/ProtocolStrategies/{protocol_strategy_id}"

    @staticmethod
    def soil_types() -> str:
        return "api/SoilTypes"

    @staticmethod
    def soil_type(soil_type_id) -> str:
        return f"api/SoilTypes/{soil_type_id}"

    @staticmethod
    def varieties() -> str:
        return "api/Varieties"

    @staticmethod
    def variety(variety_id) -> str:
        return f"api/Varieties/{variety_id}"

    @staticmethod
    def seasons() -> str:
        return "api/Seasons"

    @staticmethod
    def irrigation_strategies() -> str:
        return "api/IrrigationStrategies"

    @staticmethod
    def parameter_per_crop_family() -> str:
        return "api/ParameterPerCropFamily"

    @staticmethod
    def parameter_per_protocol_strategy() -> str:
        return "api/ParameterPerProtocolStrategy"

    @staticmethod
    def parameter_per_stage() -> str:
        return "api/ParameterPerStage"

    @staticmethod
    def parameter_per_stage_lite() -> str:
        return "api/ParameterPerStage/lite"

    @staticmethod
    def parameter_per_varieties() -> str:
        return "api/ParameterPerVarieties"

    @staticmethod
    def parameter_per_varieties_lite() -> str:
        return "api/ParameterPerVarieties/lite"

    @staticmethod
    def parameters_per_crops() -> str:
        return "api/ParametersPerCrops"

    @staticmethod
    def system_crop_protocols() -> str:
        return "api/SystemCropProtocols"
