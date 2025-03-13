"""Integration for IAMMETER-Link."""

import asyncio
import logging
from http import HTTPStatus

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, IAMMETER_API_URL, SINGLE_PHASE_SENSORS, THREE_PHASE_SENSORS

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up IAMMETER-Link component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up component from UI configuration."""
    hass.data[DOMAIN][entry.entry_id] = entry

    # Update name displayed in Home Assistant UI
    device_sn = entry.data.get("device_sn", "IAMMETER-Link")
    hass.config_entries.async_update_entry(entry, title=device_sn)

    await _start_sending_data(hass, entry)

    entry.async_on_unload(entry.add_update_listener(update_listener))
    return True


async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Re-apply settings when user updates configuration."""
    new_data = {**entry.data, **entry.options}
    hass.config_entries.async_update_entry(entry, data=new_data)
    await _start_sending_data(hass, entry)


async def _start_sending_data(hass: HomeAssistant, entry: ConfigEntry):
    """Start data sending task."""
    device_sn = entry.data.get("device_sn")
    meter_type = entry.data.get("meter_type", "single")
    session = async_get_clientsession(hass)

    async def send_data_to_iammeter():
        """Periodically get Home Assistant sensor data and send to IAMMETER Cloud."""
        while True:
            try:
                sensor_values = []
                data_valid = 0

                if meter_type == "single":
                    for sensor in SINGLE_PHASE_SENSORS:
                        sensor_id = entry.options.get(sensor, entry.data.get(sensor))
                        if sensor_id.isdigit():
                            sensor_values.append(float(sensor_id))
                        else:
                            state = hass.states.get(sensor_id)
                            if state and state.state not in [
                                None,
                                "unknown",
                                "unavailable",
                            ]:
                                sensor_values.append(float(state.state))
                            else:
                                data_valid = -1
                                break

                    sensor_data = {
                        "version": "1.1",
                        "SN": device_sn,
                        "Data": sensor_values,
                    }
                else:
                    phase_data = []
                    for phase, sensors in THREE_PHASE_SENSORS.items():
                        phase_values = []
                        for sensor in sensors:
                            sensor_id = entry.options.get(
                                sensor, entry.data.get(sensor)
                            )
                            if sensor_id.isdigit():
                                phase_values.append(float(sensor_id))
                            else:
                                state = hass.states.get(sensor_id)
                                if state and state.state not in [
                                    None,
                                    "unknown",
                                    "unavailable",
                                ]:
                                    phase_values.append(float(state.state))
                                else:
                                    data_valid = -1
                                    break
                        phase_data.append(phase_values)
                    sensor_data = {
                        "version": "1.1",
                        "SN": device_sn,
                        "Datas": phase_data,
                    }

                if data_valid != -1:
                    async with session.post(
                        IAMMETER_API_URL, json=sensor_data
                    ) as response:
                        if response.status == HTTPStatus.OK:
                            _LOGGER.info(
                                "Data successfully sent to IAMMETER Cloud: %s",
                                sensor_data,
                            )
                        else:
                            _LOGGER.error(
                                "Send failed, status code: %d, data: %s",
                                response.status,
                                sensor_data,
                            )
                else:
                    _LOGGER.warning("Invalid sensor data detected, skipping upload")
            except Exception as e:
                _LOGGER.error("Error sending data: %s", e)

            await asyncio.sleep(60)

    hass.loop.create_task(send_data_to_iammeter())
