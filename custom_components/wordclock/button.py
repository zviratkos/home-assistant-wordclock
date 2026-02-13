import aiohttp
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        WordClockButton(coordinator, entry, "reset_off", "Reset Extra Words Until Midnight", "resetew1"),
        WordClockButton(coordinator, entry, "reset_on", "Reactivate Extra Words", "resetew0"),
        WordClockButton(coordinator, entry, "refresh", "Refresh Status", "status"),
    ])

class WordClockButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, entry, uid, name, endpoint):
        super().__init__(coordinator)
        self.entry = entry
        self.endpoint = endpoint
        self._attr_unique_id = f"{entry.entry_id}_{uid}"
        self._attr_name = f"WordClock {name}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
        }

    async def async_press(self):
        host = self.entry.data["host"]
        port = self.entry.data["port"]
        url = f"http://{host}:{port}/{self.endpoint}"
        async with aiohttp.ClientSession() as session:
            await session.get(url)
        await self.coordinator.async_request_refresh()