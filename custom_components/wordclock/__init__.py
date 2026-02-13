from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .coordinator import WordClockCoordinator

PLATFORMS = ["light", "switch", "button"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    coordinator = WordClockCoordinator(
        hass,
        entry.data["host"],
        entry.data["port"],
        entry.data["scan_interval"],
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True