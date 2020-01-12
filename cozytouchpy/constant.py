from .utils import TextEnum

COZYTOUCH_BASE_URL = "https://ha110-1.overkiz.com/enduser-mobile-web/enduserAPI"

COZYTOUCH_ENDPOINTS = {
    "login": "{base_url}/login".format(base_url=COZYTOUCH_BASE_URL),
    "setup": "{base_url}/setup".format(base_url=COZYTOUCH_BASE_URL),
    "gateways": "{base_url}/setup/gateways".format(base_url=COZYTOUCH_BASE_URL),
    "devices": "{base_url}/setup/devices".format(base_url=COZYTOUCH_BASE_URL),
    "deviceInfo": "{base_url}/setup/devices/[device_url]/states".format(base_url=COZYTOUCH_BASE_URL),
    "stateInfo": "{base_url}/setup/devices/[device_url]/states/[state_name]".format(base_url=COZYTOUCH_BASE_URL),
    "apply": "{base_url}/exec/apply".format(base_url=COZYTOUCH_BASE_URL)
}

USER_AGENT = "Home assistant/Cozytouch"


class DeviceType(TextEnum):
    POD = "Pod"
    HEATER = "AtlanticElectricalHeaterWithAdjustableTemperatureSetpoint"
    HEATER_PASV = "AtlanticElectricalHeater"
    WATER_HEATER = "DomesticHotWaterProduction"
    TEMPERATURE = "TemperatureSensor"
    CONTACT = "ContactSensor"
    OCCUPANCY = "OccupancySensor"
    ELECTRECITY = "CumulativeElectricPowerConsumptionSensor"


class DeviceState(TextEnum):
    BOOST_MODE_DURATION_STATE = 'core:BoostModeDurationState'

    CONNECTIVITY_STATE = 'core:ConnectivityState'
    COUNTRY_CODE_STATE = 'core:CountryCodeState'
    LAST_ACTION_CONF_BUTTON_STATE = 'internal:LastActionConfigButtonState'
    LIGHTING_LED_POD_MODE_STATE = 'internal:LightingLedPodModeState'

    COMFORT_TARGET_TEMPERATURE_STATE = 'core:ComfortTargetTemperatureState'
    COMFORT_TEMPERATURE_STATE = "core:ComfortRoomTemperatureState"
    DHWP_SOFTWARE_VERSION_STATE = 'core:DHWPSoftwareVersionState'
    DATE_TIME_STATE = 'core:DateTimeState'
    ECO_TARGET_TEMPERATURE_STATE = 'core:EcoTargetTemperatureState'
    ECO_TEMPERATURE_STATE = "core:EcoRoomTemperatureState"
    ELECTRIC_ENERGY_CONSUMPTION_STATE = "core:ElectricEnergyConsumptionState"
    EXPECTED_NUM_SHOWER_STATE = 'core:ExpectedNumberOfShowerState'
    FROST_PROTECTION_TARGET_TEMPERATURE_STATE = 'core:FrostProtectionTargetTemperatureState'
    HALTED_TARGET_TEMPERATURE_STATE = 'core:HaltedTargetTemperatureState'
    HEATING_STATUS_STATE = 'core:HeatingStatusState'
    AWAY_STATE = 'core:HolidaysModeState'
    MANUFACTURER_NAME_STATE = 'core:ManufacturerNameState'
    MAX_SHOWER_MANUEL_MODE_STATE = 'core:MaximalShowerManualModeState'
    MAX_TEMPERATURE_MANUEL_MODE_STATE = 'core:MaximalTemperatureManualModeState'
    MIN_SHOWER_MANUEL_MODE_STATE = 'core:MinimalShowerManualModeState'
    NAME_STATE = 'core:NameState'
    NUM_TANK_STATE = 'core:NumberOfTankState'
    NUM_SHOWER_REMAINING_STATE = 'core:NumberOfShowerRemainingState'
    OPERATING_MODE_STATE = 'core:OperatingModeState'
    OCCUPANCY_STATE = "core:OccupancyState"
    ON_OFF_STATE = "core:OnOffState"
    PRIORITY_LOCK_TIMER_STATE = 'core:PriorityLockTimerState'
    RSSI_LEVEL_STATE = 'core:RSSILevelState'
    SECURED_POSITION_TEMPERATURE_STATE = 'core:SecuredPositionTemperatureState'
    STATUS_STATE = 'core:StatusState'
    TARGET_TEMPERATURE_STATE = "core:TargetTemperatureState"
    TARGETING_HEATING_LEVEL_STATE = 'io:TargetHeatingLevelState'
    TEMPERATURE_STATE = "core:TemperatureState"
    V40_WATER_VOLUME_ESTIMATION_STATE = 'core:V40WaterVolumeEstimationState'
    VERSION_STATE = 'core:VersionState'
    WATER_CONSUMPTION_STATE = 'core:WaterConsumptionState'

    ANTI_LEGIONELLOSIS_STATE = 'io:AntiLegionellosisState'
    AWAY_MODE_DURATION_STATE = 'io:AwayModeDurationState'
    BOILER_INSTALLATION_OPTION_STATE = 'io:BoilerInstallationOptionState'
    DHW_AWAY_STATE = 'io:DHWAbsenceModeState'
    DHW_BOOST_MODE_STATE = 'io:DHWBoostModeState'
    DHW_CAPACITY_STATE = 'io:DHWCapacityState'
    DHW_ERROR_STATE = 'io:DHWErrorState'
    DHW_MODE_STATE = 'io:DHWModeState'
    ELECTRIC_BOOSTER_OPERATING_TIME_STATE = 'io:ElectricBoosterOperatingTimeState'
    ELECTRIC_EXTRA_MANAGEMENT_STATE = 'io:ElectricalExtraManagementState'
    HEAT_PUMP_OPERATING_TIME_STATE = 'io:HeatPumpOperatingTimeState'
    INSTALLATION_STATE = 'io:InstallationState'
    MIDDLE_WATER_TEMPERATURE_STATE = 'io:MiddleWaterTemperatureState'
    OPERATING_MODE_CAPABILITIES_STATE = 'io:OperatingModeCapabilitiesState'
    OPERATING_RANGE_STATE = 'io:OperatingRangeState'
    POWER_CONSUMPTION_FAN_STATE = 'io:PowerConsumptionFanState'
    POWER_HEAT_ELECTRICAL_STATE = "io:PowerHeatElectricalState"
    POWER_HEAT_PUMP_STATE = "io:PowerHeatPumpState"
    PRIORITY_LOCK_LEVEL_STATE = 'io:PriorityLockLevelState'
    PRIORITY_LOCK_ORIGINATOR_STATE = 'io:PriorityLockOriginatorState'
    PROGRAMMING_SLOTS_STATE = 'io:ProgrammingSlotsState'
    RATE_MANAGEMENT_STATE = 'io:RateManagementState'
    SMART_GRID_OPTION_STATE = 'io:SmartGridOptionState'


class OnOffState(TextEnum):
    ON = "on"
    OFF = "off"


class AwayModeState(TextEnum):
    ON = "on"
    OFF = "off"


class OperatingModeState(TextEnum):
    STANDBY = "standby"
    BASIC = "basic"
    INTERNAL = "internal"
    AUTO = "auto"
    FROSTPROTECT = "frostprotection"
    MANUEL = "frostprotection"
    NORMAL = "normal"
    MAX = "max"
    PROG = "prog"
    PROGRAM = "program"


class OperatingRangeState(TextEnum):
    PAC24h = "pac24h_elec24h"
    PACPROG = "pacProg_elecProg"


class InstallationState(TextEnum):
    EXTRA_BOILER = "extraBoiler"
    EXTRA_SOLAR = "extraBoiler"
    ONLY_THERMODYNAMIC = "onlyThermodynamic"


class TargetingHeatingLevelState(TextEnum):
    ECO = "eco"
    BOOST = "boost"
    COMFORT = "comfort"
    COMFORT_ONE = "comfort-1"
    COMFORT_TWO = "comfort-2"
    FROST_PROTECTION = "frostprotection"
    SECURED = "secured"
    OFF = "off"


class DeviceCommand(TextEnum):
    GET_NAME = "getName"
    SET_ANTI_LEGIONELLOSIS = "setAntiLegionellosis"
    SET_AWAY_MODE = "setHolidays"
    SET_ALWAYS_MODE_DURATION = "setAwayModeDuration"
    SET_BOILER_INSTALLATION_OPTION = "setBoilerInstallationOption"
    SET_BOOST_MODE_DURATION = "setBoostModeDuration"
    SET_COMFORT_TEMP = "setComfortTemperature"
    SET_COMFORT_TARGET_TEMP = "setComfortTargetTemperature"
    SET_CURRENT_OPERATION_MODE = "setCurrentOperatingMode"
    SET_DATETIME = "setDateTime"
    SET_DWH_MODE = "setDHWMode"
    SET_ECO_TEMP = "setEcoTemperature"
    SET_ECO_TARGET_TEMP = "setEcoTargetTemperature"
    SET_ELECTRICAL_EXTRA_MANAGEMENT = "setElectricalExtraManagement"
    SET_EXTRACTION_OPTION = "setExtractionOption"
    SET_FROST_PROTECT_TARGET_TEMP = "setFrostProtectionTargetTemperature"
    SET_HALTED_TARGET_TEMP = "setHaltedTargetTemperature"
    SET_HEATING_LEVEL = "setHeatingLevel"
    SET_INSTALLATION = "setInstallation"
    SET_LOWERING_TEMP_PROG = "setSetpointLoweringTemperatureInProgMode"
    SET_NAME = "setName"
    SET_OPERATION_MODE = "setOperatingMode"
    SET_OPERATING_RANGE = "setOperatingRange"
    SET_PROGRAMMING_SLOT = "setProgrammingSlots"
    SET_RATE_MANAGMENT = "setRateManagement"
    SET_SMART_GRID_OPTION = "setSmartGridOption"
    SET_TARGET_TEMP = "setTargetTemperature"

    REFRESH_OPERATION_MODE = "refreshOperatingMode"
    REFRESH_ECO_TEMPERATURE = "refreshEcoTemperature"
    REFRESH_COMFORT_TEMPERATURE = "refreshComfortTemperature"
    REFRESH_HEATING_LEVEL = "refreshHeatingLevel"
    REFRESH_TARGET_TEMPERATURE = "refreshTargetTemperature"
    REFRESH_LOWERING_TEMP_PROG = "refreshSetpointLoweringTemperatureInProgMode"
    REFRESH_MANUFACTURER_NAME = "refreshManufacturerName"
    REFRESH_WATER_CONSUMPTION = "refreshWaterConsumption"
    REFRESH_BOOST_MODE_DURATION = "refreshBoostModeDuration"
    REFRESH_DHW_MODE = "refreshDHWMode"
    REFRESH_ANTI_LEGIONELLOSIS = "refreshAntiLegionellosis"
    REFRESH_ALWAYS_MODE_DURATION = "refreshAwayModeDuration"
    REFRESH_BOILER_INSTALLATION_OPTION = "refreshBoilerInstallationOption"
    REFRESH_CURRENT_OPERATING_MODE = "refreshCurrentOperatingMode"
    REFRESH_DHW_CAPACITY = "refreshDHWCapacity"
    REFRESH_DHW_ERROR = "refreshDHWError"
    REFRESH_ELECTRICAL_EXTRA_MANAGEMENT = "refreshElectricalExtraManagement"
    REFRESH_EXTRACTION_OPTION = "refreshExtractionOption"
    REFRESH_INSTALLATION = "refreshInstallation"
    REFRESH_MIDDLE_WATER_TEMPERATURE = "refreshMiddleWaterTemperature"
    REFRESH_OPERATING_MODE_CAPABILITIES = "refreshOperatingModeCapabilities"
    REFRESH_OPERATING_RANGE = "refreshOperatingRange"
    REFRESH_OPERATING_TIME = "refreshOperatingTime"
    REFRESH_PROGRAMMING_SLOT = "refreshProgrammingSlots"
    REFRESH_RATE_MANAGMENT = "refreshRateManagement"
    REFRESH_SMART_GRID_OPTION = "refreshSmartGridOption"
    REFRESH_POD_MODE = "refreshPodMode"
    REFRESH_UPDATE_STATUS = "refreshUpdateStatus"
