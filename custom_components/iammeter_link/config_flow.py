"""Config flow for iMeterLink integration."""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, DEFAULT_SINGLE_PHASE_SENSORS, DEFAULT_THREE_PHASE_SENSORS


class IAMMETERConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """IAMMETER config flow handler."""

    async def async_step_user(self, user_input=None):
        """Step 1: Select meter type."""
        errors = {}

        if user_input is not None:
            # Store device SN and meter type, then proceed to next step
            self.context["device_sn"] = user_input["device_sn"]
            self.context["meter_type"] = user_input["meter_type"]

            return await self.async_step_meter_config()  # Proceed to next step

        # Select meter type
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("device_sn"): str,
                    vol.Required("meter_type", default="single"): vol.In(
                        {"single": "Single Phase", "three": "Three Phase"}
                    ),
                }
            ),
            errors=errors,
        )

    async def async_step_meter_config(self, user_input=None):
        """Step 2: Configure sensors (dynamically based on single/three phase)."""
        device_sn = self.context["device_sn"]
        meter_type = self.context["meter_type"]

        if user_input is not None:
            # Store data and use device_sn as integration name
            return self.async_create_entry(
                title=self.context["device_sn"],
                data={
                    **user_input,
                    "device_sn": self.context["device_sn"],
                    "meter_type": meter_type,
                },
            )

        # Choose different inputs based on meter type
        if meter_type == "single":
            schema = vol.Schema(
                {
                    vol.Required(
                        sensor, default=DEFAULT_SINGLE_PHASE_SENSORS[sensor]
                    ): str
                    for sensor in DEFAULT_SINGLE_PHASE_SENSORS
                }
            )
        else:  # three phase
            schema = vol.Schema(
                {
                    vol.Required(
                        sensor, default=DEFAULT_THREE_PHASE_SENSORS[phase][sensor]
                    ): str
                    for phase in DEFAULT_THREE_PHASE_SENSORS
                    for sensor in DEFAULT_THREE_PHASE_SENSORS[phase]
                }
            )

        return self.async_show_form(step_id="meter_config", data_schema=schema)

    @staticmethod
    @callback
    def async_get_options_flow(entry: config_entries.ConfigEntry):
        """Return options flow handler."""
        return IAMMETEROptionsFlowHandler(entry)


class IAMMETEROptionsFlowHandler(config_entries.OptionsFlow):
    """IAMMETER options flow handler."""

    def __init__(self, entry: config_entries.ConfigEntry):
        self.entry = entry

    async def async_step_init(self, user_input=None):
        """Options modification UI entry point."""
        if user_input is not None:
            # Save new configuration, merge options and data
            return self.async_create_entry(title="", data=user_input)

        # Read current configuration (prioritize options, otherwise fallback to data)
        meter_type = self.entry.options.get(
            "meter_type", self.entry.data.get("meter_type", "single")
        )

        if meter_type == "single":
            schema = vol.Schema(
                {
                    vol.Required(
                        sensor,
                        default=self.entry.options.get(
                            sensor, self.entry.data.get(sensor, default_value)
                        ),
                    ): str
                    for sensor, default_value in DEFAULT_SINGLE_PHASE_SENSORS.items()
                }
            )
        else:  # three phase
            schema = vol.Schema(
                {
                    vol.Required(
                        sensor,
                        default=self.entry.options.get(
                            sensor, self.entry.data.get(sensor, default_value)
                        ),
                    ): str
                    for phase, sensors in DEFAULT_THREE_PHASE_SENSORS.items()
                    for sensor, default_value in sensors.items()
                }
            )

        return self.async_show_form(step_id="init", data_schema=schema)
