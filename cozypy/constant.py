import enum

COZYTOUCH_ENDPOINT = "https://ha110-1.overkiz.com/enduser-mobile-web/externalAPI/json/"

USER_AGENT = "Home assistant/Cozytouch"

class DeviceType(enum.Enum):
    POD = "Pod"
    HEATER = "AtlanticElectricalHeaterWithAdjustableTemperatureSetpoint"
    HEATER_PASV = "AtlanticElectricalHeater"
    TEMPERATURE = "TemperatureSensor"
    CONTACT = "ContactSensor"
    OCCUPANCY = "OccupancySensor"
    ELECTRECITY = "CumulativeElectricPowerConsumptionSensor"


class DeviceStateType(enum.Enum):
    INT = 1
    FLOAT = 2
    STR = 3
    DICT = 11
    LIST = 10


class DeviceState(enum.Enum):
    AWAY_STATE = 'core:HolidaysModeState'
    OPERATING_MODE_STATE = 'io:TargetHeatingLevelState'
    OCCUPANCY_STATE = "core:OccupancyState"
    TEMPERATURE_STATE = "core:TemperatureState"
    COMFORT_TEMPERATURE_STATE = "core:ComfortRoomTemperatureState"
    ECO_TEMPERATURE_STATE = "core:EcoRoomTemperatureState"
    ON_OFF_STATE = "core:OnOffState"
    ELECTRIC_ENERGY_CONSUMTION_STATE = "core:ElectricEnergyConsumptionState"


class DeviceCommand(enum.Enum):
    SET_OPERATION_MODE = "setHeatingLevel"
    SET_ECO_TEMP = "setEcoTemperature"
    SET_COMFORT_TEMP = "setComfortTemperature"
    SET_AWAY_MODE = "setHolidays"

    REFRESH_OPERATION_MODE = "refreshHeatingLevel"
    REFRESH_ECO_TEMPERATURE= "refreshEcoTemperature"
    REFRESH_COMFORT_TEMPERATURE = "refreshComfortTemperature"