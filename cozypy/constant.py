import enum

COZYTOUCH_ENDPOINT = "https://ha110-1.overkiz.com/enduser-mobile-web/externalAPI/json/"

USER_AGENT = "Home assistant/Cozytouch"

class DeviceType(enum.Enum):
    POD = "Pod"
    HEATER = "AtlanticElectricalHeaterWithAdjustableTemperatureSetpoint"
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
    CURRENT_TEMPERATURE_STATE = "core:TemperatureState"
    COMFORT_TEMPERATURE_STATE = "core:ComfortRoomTemperatureState"
    ECO_TEMPERATURE_STATE = "core:EcoRoomTemperatureState"
    ON_OFF_STATE = "core:OnOffState"