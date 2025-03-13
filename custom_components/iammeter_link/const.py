"""Constants for the IAMMETER-Link integration."""

DOMAIN = "iammeter_link"
IAMMETER_API_URL = "http://open.iammeter.com/api/V1/sensor/UploadSensor"

# Sensor fields for single-phase meter
SINGLE_PHASE_SENSORS = [
    "sensor_voltage",
    "sensor_current",
    "sensor_power",
    "sensor_import_energy",
    "sensor_export_energy",
]

# Sensor fields for three-phase meter
THREE_PHASE_SENSORS = {
    "A": [
        "sensor_voltage_a",
        "sensor_current_a",
        "sensor_power_a",
        "sensor_import_energy_a",
        "sensor_export_energy_a",
    ],
    "B": [
        "sensor_voltage_b",
        "sensor_current_b",
        "sensor_power_b",
        "sensor_import_energy_b",
        "sensor_export_energy_b",
    ],
    "C": [
        "sensor_voltage_c",
        "sensor_current_c",
        "sensor_power_c",
        "sensor_import_energy_c",
        "sensor_export_energy_c",
    ],
}

# Default sensors for single-phase meter
DEFAULT_SINGLE_PHASE_SENSORS = {
    "sensor_voltage": "sensor.wem3080_voltage",
    "sensor_current": "sensor.wem3080_current",
    "sensor_power": "sensor.wem3080_power",
    "sensor_import_energy": "sensor.wem3080_import_energy",
    "sensor_export_energy": "sensor.wem3080_export_energy",
}

# Default sensors for three-phase meter
DEFAULT_THREE_PHASE_SENSORS = {
    "A": {
        "sensor_voltage_a": "sensor.wem3080t_voltage_a",
        "sensor_current_a": "sensor.wem3080t_current_a",
        "sensor_power_a": "sensor.wem3080t_power_a",
        "sensor_import_energy_a": "sensor.wem3080t_import_energy_a",
        "sensor_export_energy_a": "sensor.wem3080t_export_energy_a",
    },
    "B": {
        "sensor_voltage_b": "sensor.wem3080t_voltage_b",
        "sensor_current_b": "sensor.wem3080t_current_b",
        "sensor_power_b": "sensor.wem3080t_power_b",
        "sensor_import_energy_b": "sensor.wem3080t_import_energy_b",
        "sensor_export_energy_b": "sensor.wem3080t_export_energy_b",
    },
    "C": {
        "sensor_voltage_c": "sensor.wem3080t_voltage_c",
        "sensor_current_c": "sensor.wem3080t_current_c",
        "sensor_power_c": "sensor.wem3080t_power_c",
        "sensor_import_energy_c": "sensor.wem3080t_import_energy_c",
        "sensor_export_energy_c": "sensor.wem3080t_export_energy_c",
    },
}
