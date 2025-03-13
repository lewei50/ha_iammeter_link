[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)

# IAMMETER-Link
This component will enable Home Assistant to send locally collected inverter data to IAMMETER’s **Virtual Meter**.

# IAMMETER

------

[IAMMETER](https://www.iammeter.com/) provides both a bi-directional single-phase energy meter([WEM3080](https://www.iammeter.com/products/single-phase-meter)) and a bi-directional three-phase energy monitor ([WEM3080T/WEM3050T/WEM3046T]([IAMMETER IoT(internet of things) Energy Monitoring System Supplier](https://www.iammeter.com/products))). Both of them can be integrated into Home Assistant.

# Installation

------

### Manual Installation

1. Copy `iammeter_link` folder into your custom_components folder in your hass configuration directory.
2. Restart Home Assistant.

### Installation with HACS (Home Assistant Community Store)

1. Ensure that HACS is installed.
2. Add the URL for this repository in HACS under Custom Repositories, selecting the type as Integration.
3. Search for and install the `iammeter_link` integration.
4. Restart Home Assistant.

# Configuration

It is configurable through config flow, meaning it will popup a dialog after adding the integration.

1. Head to Settings --> Devices & Services--> ADD INTEGRATION

2. Add new and search for `iammeter_link`

3. Enter the Virtual Meter SN you obtained from IAMMETER in device_sn.

4. chose meter_type:  'Single Phase' / 'Three Phase', SUNMIT

5. Change to your own sensor name(Please set the unused sensors to 0, but the set sensors must be valid in homeassistant, otherwise the data will not be uploaded to IAMMETER).

   Single Phase:

   | name                 | sensor(Change to your own sensor name) | Unit |
   | -------------------- | :------------------------------------- | :--- |
   | sensor_voltage       | sensor.wem3080_voltage                 | V    |
   | sensor_current       | sensor.wem3080_current                 | A    |
   | sensor_power         | sensor.wem3080_power                   | W    |
   | sensor_import_energy | sensor.wem3080_import_energy           | kWh  |
   | sensor_export_energy | sensor.wem3080_export_energy           | kWh  |

   Three Phase:

   | name                     | sensor(Change to your own sensor name) | Unit |
   | ------------------------ | :------------------------------------- | :--- |
   | sensor_voltage_a         | sensor.wem3080t_voltage_a              | V    |
   | sensor_current_a         | sensor.wem3080t_current_a              | A    |
   | sensor_power_a           | sensor.wem3080t_power_a                | W    |
   | sensor_import_energy_a   | sensor.wem3080t_import_energy_a        | kWh  |
   | sensor_export_energy_a   | sensor.wem3080t_export_energy_a        | kWh  |
   | sensor_voltage_b         | sensor.wem3080t_voltage_b              | V    |
   | sensor_current_b         | sensor.wem3080t_current_b              | A    |
   | sensor_power_b           | sensor.wem3080t_power_b                | W    |
   | sensor_import_energy_b   | sensor.wem3080t_import_energy_b        | kWh  |
   | sensor_export_energy_b   | sensor.wem3080t_export_energy_b        | kWh  |
   | sensor_voltage_c         | sensor.wem3080t_voltage_c              | V    |
   | sensor_current_c         | sensor.wem3080t_current_c              | A    |
   | sensor_power_c           | sensor.wem3080t_power_c                | W    |
   | sensor_import_energy_c   | sensor.wem3080t_import_energy_c        | kWh  |
   | sensor_export_energy_c   | sensor.wem3080t_export_energy_c        | kWh  |

6. SUNMIT
