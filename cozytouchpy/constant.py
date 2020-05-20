"""Constants."""

from .utils import TextEnum

COZYTOUCH_BASE_URL = "https://ha110-1.overkiz.com/enduser-mobile-web/enduserAPI"

COZYTOUCH_ENDPOINTS = {
    "login": "{base_url}/login".format(base_url=COZYTOUCH_BASE_URL),
    "setup": "{base_url}/setup".format(base_url=COZYTOUCH_BASE_URL),
    "gateways": "{base_url}/setup/gateways".format(base_url=COZYTOUCH_BASE_URL),
    "devices": "{base_url}/setup/devices".format(base_url=COZYTOUCH_BASE_URL),
    "deviceInfo": "{base_url}/setup/devices/[device_url]/states".format(
        base_url=COZYTOUCH_BASE_URL
    ),
    "stateInfo": "{base_url}/setup/devices/[device_url]/states/[state_name]".format(
        base_url=COZYTOUCH_BASE_URL
    ),
    "apply": "{base_url}/exec/apply".format(base_url=COZYTOUCH_BASE_URL),
}

USER_AGENT = "Home assistant/Cozytouch"
API_THROTTLE = 60  # Delay minimum between API call


class DeviceType(TextEnum):
    """Device type."""

    POD = "Pod"
    HEATER = "AtlanticElectricalHeaterWithAdjustableTemperatureSetpoint"
    PILOT_WIRE_INTERFACE = "AtlanticElectricalHeater"
    WATER_HEATER = "DomesticHotWaterProduction"
    TEMPERATURE = "TemperatureSensor"
    CONTACT = "ContactSensor"
    OCCUPANCY = "OccupancySensor"
    ELECTRECITY = "CumulativeElectricPowerConsumptionSensor"
    APC_HEAT_PUMP = "AtlanticPassAPCHeatPump"
    APC_WATER_HEATER = "AtlanticPassAPCDHW"
    APC_HEATING_AND_COOLING_ZONE = "AtlanticPassAPCHeatingAndCoolingZone"

    @classmethod
    def sensors(cls):
        """Sensors method."""
        return [cls.TEMPERATURE, cls.CONTACT, cls.OCCUPANCY, cls.ELECTRECITY]


class DeviceState(TextEnum):
    """Device state."""

    ABSENCE_COOLING_TARGET_TEMPERATURE_STATE = (
        "core:AbsenceCoolingTargetTemperatureState"
    )
    ABSENCE_END_DATE_STATE = "core:AbsenceEndDateState"
    ABSENCE_HEATING_TARGET_TEMPERATURE_STATE = (
        "core:AbsenceHeatingTargetTemperatureState"
    )
    ABSENCE_START_DATE_STATE = "core:AbsenceStartDateState"
    ACTIVE_COOLING_TIME_PROGRAM_STATE = "core:ActiveCoolingTimeProgramState"
    ACTIVE_HEATING_TIME_PROGRAM_STATE = "core:ActiveHeatingTimeProgramState"
    AWAY_STATE = "core:HolidaysModeState"
    BOOST_ELECTRIC_POWER_CONSUMPTION_STATE = (
        "core:BoostElectricPowerConsumptionState"  # int
    )
    BOOST_END_DATE_STATE = "core:BoostEndDateState"  # dict
    BOOST_MODE_DURATION_STATE = "core:BoostModeDurationState"  # int
    BOOST_ON_OFF_STATE = "core:BoostOnOffState"
    BOOST_START_DATE_STATE = "core:BoostStartDateState"  # dict
    BOTTOM_TANK_WATER_TEMPERATURE_STATE = "core:BottomTankWaterTemperatureState"
    COMFORT_COOLING_TARGET_TEMPERATURE_STATE = (
        "core:ComfortCoolingTargetTemperatureState"
    )
    COMFORT_HEATING_TARGET_TEMPERATURE_STATE = (
        "core:ComfortHeatingTargetTemperatureState"
    )
    COMFORT_TARGET_TEMPERATURE_STATE = "core:ComfortTargetTemperatureState"
    COMFORT_TEMPERATURE_STATE = "core:ComfortRoomTemperatureState"
    CONNECTIVITY_STATE = "core:ConnectivityState"
    CONTACT_STATE = "core:ContactState"
    CONTROL_WATER_TARGET_TEMPERATURE_STATE = (
        "core:ControlWaterTargetTemperatureState"  # int
    )
    COOLING_ON_OFF_STATE = "core:CoolingOnOffState"
    COUNTRY_CODE_STATE = "core:CountryCodeState"
    DATE_TIME_STATE = "core:DateTimeState"  # dict
    DEROGATED_TARGET_TEMPERATURE_STATE = "core:DerogatedTargetTemperatureState"
    DEROGATION_ON_OFF_STATE = "core:DerogationOnOffState"
    DHW_DEROGATION_AVAILABILITY_STATE = "core:DHWDerogationAvailabilityState"
    DHW_ON_OFF_STATE = "core:DHWOnOffState"
    DHWP_SOFTWARE_VERSION_STATE = "core:DHWPSoftwareVersionState"  # string
    ECO_COOLING_TARGET_TEMPERATURE_STATE = "core:EcoCoolingTargetTemperatureState"
    ECO_HEATING_TARGET_TEMPERATURE_STATE = "core:EcoHeatingTargetTemperatureState"
    ECO_TARGET_TEMPERATURE_STATE = "core:EcoTargetTemperatureState"
    ECO_TEMPERATURE_STATE = "core:EcoRoomTemperatureState"
    ECS_POWER_CONSUMPTION_EXTRA1_STATE = "core:ECSPowerConsumptionExtra1State"
    ECS_POWER_CONSUMPTION_EXTRA2_STATE = "core:ECSPowerConsumptionExtra2State"
    ECS_POWER_CONSUMPTION_EXTRA3_STATE = "core:ECSPowerConsumptionExtra3State"
    ECS_POWER_CONSUMPTION_STATE = "core:ECSPowerConsumptionState"
    ELECTRIC_ENERGY_CONSUMPTION_STATE = "core:ElectricEnergyConsumptionState"
    ERROR_CODE_STATE = "core:ErrorCodeState"
    EXPECTED_NUM_SHOWER_STATE = "core:ExpectedNumberOfShowerState"  # int
    FROST_PROTECTION_TARGET_TEMPERATURE_STATE = (
        "core:FrostProtectionTargetTemperatureState"
    )
    HALTED_TARGET_TEMPERATURE_STATE = "core:HaltedTargetTemperatureState"
    HEATING_DEROGATION_AVAILABILITY_STATE = "core:HeatingDerogationAvailabilityState"
    HEATING_ON_OFF_STATE = "core:HeatingOnOffState"
    HEATING_POWER_CONSUMPTION_EXTRA1_STATE = "core:HeatingPowerConsumptionExtra1State"
    HEATING_POWER_CONSUMPTION_EXTRA2_STATE = "core:HeatingPowerConsumptionExtra2State"
    HEATING_POWER_CONSUMPTION_EXTRA3_STATE = "core:HeatingPowerConsumptionExtra3State"
    HEATING_POWER_CONSUMPTION_STATE = "core:HeatingPowerConsumptionState"
    HEATING_STATUS_STATE = "core:HeatingStatusState"  # bool off
    LAST_ACTION_CONF_BUTTON_STATE = "internal:LastActionConfigButtonState"
    LIGHTING_LED_POD_MODE_STATE = "internal:LightingLedPodModeState"
    MANUFACTURER_NAME_STATE = "core:ManufacturerNameState"  # string
    MAX_SHOWER_MANUEL_MODE_STATE = "core:MaximalShowerManualModeState"  # int
    MAX_TEMPERATURE_MANUEL_MODE_STATE = "core:MaximalTemperatureManualModeState"  # int
    MIDDLE_WATER_TEMPERATURE_IN_STATE = "core:MiddleWaterTemperatureInState"  # float
    MIN_SHOWER_MANUEL_MODE_STATE = "core:MinimalShowerManualModeState"  # int
    MIN_TEMPERATURE_MANUEL_MODE_STATE = "core:MinimalTemperatureManualModeState"  # int
    NAME_STATE = "core:NameState"  # string
    NUM_SHOWER_REMAINING_STATE = "core:NumberOfShowerRemainingState"  # int
    NUM_TANK_STATE = "core:NumberOfTankState"  # int
    OCCUPANCY_STATE = "core:OccupancyState"
    ON_OFF_STATE = "core:OnOffState"
    OPERATING_MODE_STATE = "core:OperatingModeState"  # dict -> class OperatingModeState
    POWER_HEAT_ELECTRICAL_IN_STATE = "core:PowerHeatElectricalInState"  # int
    PRIORITY_LOCK_TIMER_STATE = "core:PriorityLockTimerState"
    PRODUCT_MODEL_NAME_STATE = "core:ProductModelNameState"
    PROGRAMMING_AVAILABLE_STATE = "core:ProgrammingAvailableState"  # int
    RSSI_LEVEL_STATE = "core:RSSILevelState"  # int 0-100
    SECURED_POSITION_TEMPERATURE_STATE = "core:SecuredPositionTemperatureState"
    STATUS_STATE = "core:StatusState"  # string available,unavailable
    STOP_RELAUNCH_STATE = "core:StopRelaunchState"
    TARGET_DHW_TEMPERATURE_STATE = "core:TargetDHWTemperatureState"
    TARGET_TEMPERATURE_STATE = "core:TargetTemperatureState"  # float
    TEMPERATURE_STATE = "core:TemperatureState"  # float
    THERMAL_CONFIGURATION_STATE = "core:ThermalConfigurationState"
    TIME_PROGRAM1_STATE = "core:TimeProgram1State"
    TIME_PROGRAM2_STATE = "core:TimeProgram2State"
    TIME_PROGRAM3_STATE = "core:TimeProgram3State"
    TIME_PROGRAM4_STATE = "core:TimeProgram4State"
    V40_WATER_VOLUME_ESTIMATION_STATE = "core:V40WaterVolumeEstimationState"  # int
    VERSION_STATE = "core:VersionState"  # int
    WATER_CONSUMPTION_STATE = "core:WaterConsumptionState"  # int
    WATER_TARGET_TEMPERATURE_STATE = "core:WaterTargetTemperatureState"  # int
    WATER_TEMPERATURE_STATE = "core:WaterTemperatureState"  # int
    ZONES_NUMBER_STATE = "core:ZonesNumberState"

    # Input/Output
    ABSENCE_SCHEDULING_AVAILABILITY_STATE = "io:AbsenceSchedulingAvailabilityState"
    ABSENCE_SCHEDULING_MODE_STATE = "io:AbsenceSchedulingModeState"
    ANTI_LEGIONELLOSIS_STATE = "io:AntiLegionellosisState"  # bool 0/1
    AWAY_MODE_DURATION_STATE = "io:AwayModeDurationState"  # bool 0/1
    BOILER_INSTALLATION_OPTION_STATE = "io:BoilerInstallationOptionState"  # dict
    COOLING_INTERNAL_SCHEDULING_AVAILABILITY_STATE = (
        "io:CoolingInternalSchedulingAvailabilityState"
    )
    DEROGATION_REMAINING_TIME_STATE = "io:DerogationRemainingTimeState"
    DHW_AVAILABILITY_STATE = "io:DHWAvailabilityState"
    DHW_AWAY_STATE = "io:DHWAbsenceModeState"  # string off,on,prog
    DHW_BOOST_MODE_STATE = "io:DHWBoostModeState"  # string off,on,prog
    DHW_CAPACITY_STATE = "io:DHWCapacityState"  # float
    DHW_ERROR_STATE = "io:DHWErrorState"  # dict
    DHW_MODE_STATE = "io:DHWModeState"  # string
    ELECTRIC_BOOSTER_OPERATING_TIME_STATE = (
        "io:ElectricBoosterOperatingTimeState"  # int
    )
    ELECTRIC_EXTRA_MANAGEMENT_STATE = (
        "io:ElectricalExtraManagementState"  # string auto,deactive
    )
    ENERGY_CONSUMPTION_AVAILABILITY_STATE = "io:EnergyConsumptionAvailabilityState"
    EXTRACTION_OPTION_STATE = "io:ExtractionOptionState"  # string  fastExtractionSpeed,lowExtractionSpeed,noExtraction
    HEATING_INTERNAL_SCHEDULING_AVAILABILITY_STATE = (
        "io:HeatingInternalSchedulingAvailabilityState"
    )
    HEAT_PUMP_OPERATING_TIME_STATE = "io:HeatPumpOperatingTimeState"  # int
    INSTALLATION_STATE = "io:InstallationState"  # string -> class InstallationState
    LAST_PASS_APC_OPERATING_MODE_STATE = "io:LastPassAPCOperatingModeState"
    MIDDLE_WATER_TEMPERATURE_STATE = "io:MiddleWaterTemperatureState"  # float
    MODEL_STATE = "io:ModelState"
    OPERATING_MODE_CAPABILITIES_STATE = "io:OperatingModeCapabilitiesState"
    OPERATING_RANGE_STATE = "io:OperatingRangeState"  # string
    PASS_APC_COOLING_MODE_STATE = "io:PassAPCCoolingModeState"
    PASS_APC_COOLING_PROFILE_STATE = "io:PassAPCCoolingProfileState"
    PASS_APC_DHW_CONFIGURATION_STATE = "io:PassAPCDHWConfigurationState"
    PASS_APC_DHW_MODE_STATE = "io:PassAPCDHWModeState"
    PASS_APC_DHW_PROFILE_STATE = "io:PassAPCDHWProfileState"
    PASS_APC_HEATING_MODE_STATE = "io:PassAPCHeatingModeState"
    PASS_APC_HEATING_PROFILE_STATE = "io:PassAPCHeatingProfileState"
    PASS_APC_OPERATING_MODE_STATE = "io:PassAPCOperatingModeState"
    PASS_APC_PRODUCT_TYPE_STATE = "io:PassAPCProductTypeState"
    POWER_CONSUMPTION_FAN_STATE = "io:PowerConsumptionFanState"  # int
    POWER_HEAT_ELECTRICAL_STATE = "io:PowerHeatElectricalState"  # int
    POWER_HEAT_PUMP_STATE = "io:PowerHeatPumpState"  # int
    PRIORITY_LOCK_LEVEL_STATE = (
        "io:PriorityLockLevelState"  # string -> class PriorityLockLevelState
    )
    PRIORITY_LOCK_ORIGINATOR_STATE = (
        "io:PriorityLockOriginatorState"  # string -> class PriorityLockOriginatorState
    )
    PROGRAMMING_SLOTS_STATE = "io:ProgrammingSlotsState"  # dict
    RATE_MANAGEMENT_STATE = (
        "io:RateManagementState"  # string forbidden,no,recommended,unsuitable,wanted
    )
    SMART_GRID_OPTION_STATE = "io:SmartGridOptionState"  # string active,deactive
    TARGETING_HEATING_LEVEL_STATE = "io:TargetHeatingLevelState"
    THERMAL_SCHEDULING_AVAILABILITY_STATE = "io:ThermalSchedulingAvailabilityState"
    THERMAL_SCHEDULING_MODE_STATE = "io:ThermalSchedulingModeState"


class OnOffState(TextEnum):
    """Set state."""

    ON = "on"
    OFF = "off"


class AwayModeState(TextEnum):
    """Set away mode."""

    ON = "on"
    OFF = "off"


class OperatingModeState(TextEnum):
    """Set operation mode."""

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
    """Set operation range."""

    PAC24h = "pac24h_elec24h"
    PACPROG = "pacProg_elecProg"


class PriorityLockLevelState(TextEnum):
    """Priority Locke level."""

    COMFORTL1 = "comfortLevel1"
    COMFORTL2 = "comfortLevel2"
    COMFORTL3 = "comfortLevel3"
    COMFORTL4 = "comfortLevel4"
    ENVPROTECT = "environmentProtection"
    HUMPROTECT = "humanProtection"
    USERL1 = "userLevel1"
    USERL2 = "userLevel2"


class PriorityLockOriginatorState(TextEnum):
    """Priority Lock Originitor."""

    LSC = "LSC"
    SAAC = "SAAC"
    SFC = "SFC"
    UPS = "UPS"
    EXTERNALGATEWAY = "externalGateway"
    LOCALUSER = "localUser"
    MYSELF = "myself"
    RAIN = "rain"
    SECURITY = "security"
    TEMPERATURE = "temperature"
    TIMER = "timer"
    USER = "user"
    WIND = "wind"


class InstallationState(TextEnum):
    """Set installation state."""

    EXTRA_BOILER = "extraBoiler"
    EXTRA_SOLAR = "extraSolar"
    ONLY_THERMODYNAMIC = "onlyThermodynamic"


class TargetingHeatingLevelState(TextEnum):
    """Set targeting heating level state."""

    ECO = "eco"
    BOOST = "boost"
    COMFORT = "comfort"
    COMFORT_ONE = "comfort-1"
    COMFORT_TWO = "comfort-2"
    FROST_PROTECTION = "frostprotection"
    SECURED = "secured"
    OFF = "off"


class DeviceCommand(TextEnum):
    """Commande device."""

    DELAY_STOP_IDENTIFY = "delayedStopIdentify"
    GET_NAME = "getName"
    SET_ABSENCE_COOLING_TARGET_TEMPERATURE = "setAbsenceCoolingTargetTemperature"
    SET_ABSENCE_END_DATE = "setAbsenceEndDate"
    SET_ABSENCE_END_DATE_TIME = "setAbsenceEndDateTime"
    SET_ABSENCE_HEATING_TARGET_TEMPERATURE = "setAbsenceHeatingTargetTemperature"
    SET_ABSENCE_MODE = "setAbsenceMode"
    SET_ABSENCE_START_DATE = "setAbsenceStartDate"
    SET_ABSENCE_START_DATE_TIME = "setAbsenceStartDateTime"
    SET_ACTIVE_COOLING_TIME_PROGRAM = "setActiveCoolingTimeProgram"
    SET_ACTIVE_HEATING_TIME_PROGRAM = "setActiveHeatingTimeProgram"
    SET_ANTI_LEGIONELLOSIS = "setAntiLegionellosis"
    SET_AWAY_MODE = "setHolidays"
    SET_AWAYS_MODE_DURATION = "setAwayModeDuration"
    SET_BOILER_INSTALLATION_OPTION = "setBoilerInstallationOption"
    SET_BOOST_END_DATE = "setBoostEndDate"
    SET_BOOST_MODE = "setBoostMode"
    SET_BOOST_MODE_DURATION = "setBoostModeDuration"
    SET_BOOST_ON_OFF_STATE = "setBoostOnOffState"
    SET_BOOST_START_DATE = "setBoostStartDate"
    SET_CALENDAR = "setCalendar"
    SET_COMFORT_COOLING_TARGET_TEMPERATURE = "setComfortCoolingTargetTemperature"
    SET_COMFORT_HEATING_TARGET_TEMPERATURE = "setComfortHeatingTargetTemperature"
    SET_COMFORT_TARGET_DHW_TEMPERATURE = "setComfortTargetDHWTemperature"
    SET_COMFORT_TARGET_TEMP = "setComfortTargetTemperature"
    SET_COMFORT_TEMP = "setComfortTemperature"
    SET_COOLING_ON_OFF_STATE = "setCoolingOnOffState"
    SET_COUNTRY_CODE = "setCountryCode"
    SET_CURRENT_OPERATION_MODE = "setCurrentOperatingMode"
    SET_DATETIME = "setDateTime"
    SET_DEROGATED_TARGET_TEMPERATURE = "setDerogatedTargetTemperature"
    SET_DEROGATION_ON_OFF_STATE = "setDerogationOnOffState"
    SET_DEROGATION_TIME = "setDerogationTime"
    SET_DHW_ON_OFF_STATE = "setDHWOnOffState"
    SET_DWH_MODE = "setDHWMode"
    SET_ECO_COOLING_TARGET_TEMPERATURE = "setEcoCoolingTargetTemperature"
    SET_ECO_HEATING_TARGET_TEMPERATURE = "setEcoHeatingTargetTemperature"
    SET_ECO_TARGET_DHW_TEMPERATURE = "setEcoTargetDHWTemperature"
    SET_ECO_TARGET_TEMP = "setEcoTargetTemperature"
    SET_ECO_TEMP = "setEcoTemperature"
    SET_ELECTRICAL_EXTRA_MANAGEMENT = "setElectricalExtraManagement"
    SET_EXPECTED_NUM_SHOWER = "setExpectedNumberOfShower"
    SET_EXTRACTION_OPTION = "setExtractionOption"
    SET_FROST_PROTECT_TARGET_TEMP = "setFrostProtectionTargetTemperature"
    SET_HALTED_TARGET_TEMP = "setHaltedTargetTemperature"
    SET_HEATING_LEVEL = "setHeatingLevel"
    SET_HEATING_ON_OFF_STATE = "setHeatingOnOffState"
    SET_INSTALLATION = "setInstallation"
    SET_LIGHTING_LED_POD_MODE = "setLightingLedPodMode"
    SET_LOWERING_TEMP_PROG = "setSetpointLoweringTemperatureInProgMode"
    SET_NAME = "setName"
    SET_OPERATING_RANGE = "setOperatingRange"
    SET_OPERATION_MODE = "setOperatingMode"
    SET_PASS_APC_COOLING_MODE = "setPassAPCCoolingMode"
    SET_PASS_APC_DHW_MODE = "setPassAPCDHWMode"
    SET_PASS_APC_HEATING_MODE = "setPassAPCHeatingMode"
    SET_PASS_APC_OPERATING_MODE = "setPassAPCOperatingMode"
    SET_POD_LED_OFF = "setPodLedOff"
    SET_POD_LED_ON = "setPodLedOn"
    SET_PROGRAMMING_SLOT = "setProgrammingSlots"
    SET_RATE_MANAGMENT = "setRateManagement"
    SET_SMART_GRID_OPTION = "setSmartGridOption"
    SET_TARGET_TEMP = "setTargetTemperature"
    SET_TIME_PROGRAM_BY_ID = "setTimeProgramById"
    SET_WATER_TARGET_TEMPERATURE = "setWaterTargetTemperature"
    SET_WATER_TEMPERATURE = "setWaterTemperature"

    REFRESH_ABSENCE_END_DATE = "refreshAbsenceEndDate"
    REFRESH_ABSENCE_MODE = "refreshAbsenceMode"
    REFRESH_ABSENCE_SCHEDULING_AVAILABILITY = "refreshAbsenceSchedulingAvailability"
    REFRESH_ABSENCE_START_DATE = "refreshAbsenceStartDate"
    REFRESH_ANTI_LEGIONELLOSIS = "refreshAntiLegionellosis"
    REFRESH_AWAYS_MODE_DURATION = "refreshAwayModeDuration"
    REFRESH_BOILER_INSTALLATION_OPTION = "refreshBoilerInstallationOption"
    REFRESH_BOOST_END_DATE = "refreshBoostEndDate"
    REFRESH_BOOST_MODE = "refreshBoostMode"
    REFRESH_BOOST_MODE_DURATION = "refreshBoostModeDuration"
    REFRESH_BOOST_START_DATE = "refreshBoostStartDate"
    REFRESH_BOTTOM_TANK_WATER_TEMPERATURE = "refreshBottomTankWaterTemperature"
    REFRESH_COMFORT_COOLING_TARGET_TEMPERATURE = (
        "refreshComfortCoolingTargetTemperature"
    )
    REFRESH_COMFORT_HEATING_TARGET_TEMPERATURE = (
        "refreshComfortHeatingTargetTemperature"
    )
    REFRESH_COMFORT_TARGET_DHW_TEMPERATURE = "refreshComfortTargetDHWTemperature"
    REFRESH_COMFORT_TEMPERATURE = "refreshComfortTemperature"
    REFRESH_CURRENT_OPERATING_MODE = "refreshCurrentOperatingMode"
    REFRESH_DEROGATION_REMAINING_TIME = "refreshDerogationRemainingTime"
    REFRESH_DEVICE_SERIAL_NUMBER = "refreshDeviceSerialNumber"
    REFRESH_DHW_AVAILABILITY = "refreshDHWAvailability"
    REFRESH_DHW_CAPACITY = "refreshDHWCapacity"
    REFRESH_DHW_CONFIGURATION = "refreshDHWConfiguration"
    REFRESH_DHW_DEROGATION_AVAILABILITY = "refreshDHWDerogationAvailability"
    REFRESH_DHW_ERROR = "refreshDHWError"
    REFRESH_DHW_MODE = "refreshDHWMode"
    REFRESH_DHW_ON_OFF_STATE = "refreshDHWOnOffState"
    REFRESH_ECO_COOLING_TARGET_TEMPERATURE = "refreshEcoCoolingTargetTemperature"
    REFRESH_ECO_HEATING_TARGET_TEMPERATURE = "refreshEcoHeatingTargetTemperature"
    REFRESH_ECO_TARGET_DHW_TEMPERATURE = "refreshEcoTargetDHWTemperature"
    REFRESH_ECO_TEMPERATURE = "refreshEcoTemperature"
    REFRESH_ELECTRICAL_EXTRA_MANAGEMENT = "refreshElectricalExtraManagement"
    REFRESH_ELECTRIC_ENERGY_CONSUMPTION = "refreshElectricEnergyConsumption"
    REFRESH_ENERGY_CONSUMPTION_AVAILABILITY = "refreshEnergyConsumptionAvailability"
    REFRESH_ERROR_CODE = "refreshErrorCode"
    REFRESH_EXPECTED_NUM_SHOWER = "refreshExpectedNumberOfShower"
    REFRESH_EXTRACTION_OPTION = "refreshExtractionOption"
    REFRESH_HEATING_DEROGATION_AVAILABILITY = "refreshHeatingDerogationAvailability"
    REFRESH_HEATING_LEVEL = "refreshHeatingLevel"
    REFRESH_INSTALLATION = "refreshInstallation"
    REFRESH_LOWERING_TEMP_PROG = "refreshSetpointLoweringTemperatureInProgMode"
    REFRESH_MANUFACTURER_NAME = "refreshManufacturerName"
    REFRESH_MIDDLE_WATER_TEMPERATURE = "refreshMiddleWaterTemperature"
    REFRESH_MIDDLE_WATER_TEMPERATURE_IN = "refreshMiddleWaterTemperatureIn"
    REFRESH_OPERATING_MODE_CAPABILITIES = "refreshOperatingModeCapabilities"
    REFRESH_OPERATING_MODE = "refreshOperatingMode"
    REFRESH_OPERATING_RANGE = "refreshOperatingRange"
    REFRESH_OPERATING_TIME = "refreshOperatingTime"
    REFRESH_OPERATION_MODE = "refreshOperatingMode"
    REFRESH_OUTSIDE_TEMPERATURE = "refreshOutsideTemperature"
    REFRESH_OUTSIDE_TEMPERATURE_SENSOR_AVAILABILITY = (
        "refreshOutsideTemperatureSensorAvailability"
    )
    REFRESH_PASS_APC_COOLING_MODE = "refreshPassAPCCoolingMode"
    REFRESH_PASS_APC_COOLING_PROFILE = "refreshPassAPCCoolingProfile"
    REFRESH_PASS_APC_DHW_MODE = "refreshPassAPCDHWMode"
    REFRESH_PASS_APC_DHW_PROFILE = "refreshPassAPCDHWProfile"
    REFRESH_PASS_APC_HEATING_MODE = "refreshPassAPCHeatingMode"
    REFRESH_PASS_APC_HEATING_PROFILE = "refreshPassAPCHeatingProfile"
    REFRESH_POD_MODE = "refreshPodMode"
    REFRESH_PRODUCT_TYPE = "refreshProductType"
    REFRESH_PROGRAMMING_SLOT = "refreshProgrammingSlots"
    REFRESH_RATE_MANAGMENT = "refreshRateManagement"
    REFRESH_SMART_GRID_OPTION = "refreshSmartGridOption"
    REFRESH_TARGET_DHW_TEMPERATURE = "refreshTargetDHWTemperature"
    REFRESH_TARGET_TEMPERATURE = "refreshTargetTemperature"
    REFRESH_THERMAL_SCHEDULING_AVAILABILITY = "refreshThermalSchedulingAvailability"
    REFRESH_TIME_PROGRAM_BY_ID = "refreshTimeProgramById"
    REFRESH_UPDATE_STATUS = "refreshUpdateStatus"
    REFRESH_WATER_CONSUMPTION = "refreshWaterConsumption"
    REFRESH_WATER_TARGET_TEMPERATURE = "refreshWaterTargetTemperature"
    REFRESH_WATER_TEMPERATURE = "refreshWaterTemperature"
    REFRESH_ZONES_NUMBER = "refreshZonesNumber"
    REFRESH_ZONES_PASS_APC_COOLING_PROFILE = "refreshZonesPassAPCCoolingProfile"
    REFRESH_ZONES_PASS_APC_HEATING_PROFILE = "refreshZonesPassAPCHeatingProfile"
    REFRESH_ZONES_TARGET_TEMPERATURE = "refreshZonesTargetTemperature"
    REFRESH_ZONES_TEMPERATURE = "refreshZonesTemperature"
    REFRESH_ZONES_TEMPERATURE_SENSOR_AVAILABILITY = (
        "refreshZonesTemperatureSensorAvailability"
    )
    REFRESH_ZONES_THERMAL_CONFIGURATION = "refreshZonesThermalConfiguration"
