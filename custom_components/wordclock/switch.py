import aiohttp
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        WordClockExtraWord(coordinator, entry, i)
        for i in range(1, 13)
    ])

class WordClockExtraWord(CoordinatorEntity, SwitchEntity):
    def __init__(self, coordinator, entry, number):
        super().__init__(coordinator)
        self.entry = entry
        self.number = number
        self._attr_unique_id = f"{entry.entry_id}_ew_{number}"
        self._attr_name = f"WordClock EW{number}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
        }

    @property
    def is_on(self):
        return self.coordinator.data.get(f"ew{self.number}", 0) == 1

    async def async_turn_on(self, **kwargs):
        host = self.entry.data["host"]
        port = self.entry.data["port"]
        url = f"http://{host}:{port}/ew/?ew{self.number}=1"
        async with aiohttp.ClientSession() as session:
            await session.get(url)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        host = self.entry.data["host"]
        port = self.entry.data["port"]
        url = f"http://{host}:{port}/ew/?ew{self.number}=0"
        async with aiohttp.ClientSession() as session:
            await session.get(url)
        await self.coordinator.async_request_refresh()