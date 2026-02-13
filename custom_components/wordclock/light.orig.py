import aiohttp
from homeassistant.components.light import LightEntity, ColorMode
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        WordClockLight(coordinator, entry, "time"),
        WordClockLight(coordinator, entry, "background"),
    ])

class WordClockLight(CoordinatorEntity, LightEntity):
    _attr_supported_color_modes = {ColorMode.RGB}
    _attr_color_mode = ColorMode.RGB

    def __init__(self, coordinator, entry, mode):
        super().__init__(coordinator)
        self.entry = entry
        self.mode = mode
        self._attr_unique_id = f"{entry.entry_id}_{mode}"
        self._attr_name = f"WordClock {mode}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": "WordClock",
            "manufacturer": "AWSW",
            "model": "WordClock 2024",
        }

    @property
    def rgb_color(self):
        d = self.coordinator.data
        if self.mode == "time":
            return (d["R-Time"], d["G-Time"], d["B-Time"])
        return (d["R-Back"], d["G-Back"], d["B-Back"])

    @property
    def brightness(self):
        intensity = self.coordinator.data["INTENSITY"]
        return int(intensity * 255 / 100)

    @property
    def is_on(self):
        return self.coordinator.data["INTENSITY"] > 0

    async def async_turn_on(self, **kwargs):
        host = self.entry.data["host"]
        port = self.entry.data["port"]

        brightness = kwargs.get("brightness", self.brightness)
        rgb = kwargs.get("rgb_color", self.rgb_color)

        intensity = int(brightness * 100 / 255)
        r,g,b = rgb

        url = (
            f"http://{host}:{port}/config?"
            f"R-Time={r}&G-Time={g}&B-Time={b}"
            f"&INTENSITY={intensity}&INTENSITYviaWEB=1"
        )

        async with aiohttp.ClientSession() as session:
            await session.get(url)

        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        host = self.entry.data["host"]
        port = self.entry.data["port"]

        url = f"http://{host}:{port}/config?INTENSITY=0&INTENSITYviaWEB=1"

        async with aiohttp.ClientSession() as session:
            await session.get(url)

        await self.coordinator.async_request_refresh()