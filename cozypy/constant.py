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

class DeviceState(enum.Enum):
    TEMPERATURE_STATE = "core:TemperatureState"