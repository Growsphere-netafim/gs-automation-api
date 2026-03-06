class LookupServiceEndpoints:
    @staticmethod
    def countries() -> str:
        return "api/Countries"

    @staticmethod
    def irrigation_methods() -> str:
        return "api/IrrigationMethods"

    @staticmethod
    def irrigation_method(irrigation_method_id) -> str:
        return f"api/IrrigationMethods/{irrigation_method_id}"

    @staticmethod
    def measure_units() -> str:
        return "api/MeasureUnits"

    @staticmethod
    def measure_unit(uom_id) -> str:
        return f"api/MeasureUnits/{uom_id}"

    @staticmethod
    def states(country_iso_symbol: str) -> str:
        return f"api/States/{country_iso_symbol}"

    @staticmethod
    def timezones() -> str:
        return "api/Timezones"

    @staticmethod
    def timezones_windows() -> str:
        return "api/Timezones/windows"

    @staticmethod
    def timezones_iana() -> str:
        return "api/Timezones/iana"
