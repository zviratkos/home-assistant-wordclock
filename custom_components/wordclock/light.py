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
        self._attr_name = f"WordClock Color {mode.capitalize()}"

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
        d = self.coordinator.data or {}
        if self.mode == "time":
            return (
                d.get("R-Time", 255),
                d.get("G-Time", 255),
                d.get("B-Time", 255),
            )
        return (
            d.get("R-Back", 0),
            d.get("G-Back", 0),
            d.get("B-Back", 0),
        )

    @property
    def brightness(self):
        intensity = (self.coordinator.data or {}).get("INTENSITY", 0)
        return int(intensity * 255 / 50)

    @property
    def is_on(self):
        return (self.coordinator.data or {}).get("INTENSITY", 0) > 0

    async def async_turn_on(self, **kwargs):
        host = self.entry.data["host"]
        port = self.entry.data["port"]

        brightness = kwargs.get("brightness", self.brightness)
        rgb = kwargs.get("rgb_color", self.rgb_color)

        intensity = int(brightness * 50 / 255)
        r, g, b = rgb

        if self.mode == "time":
            # Time text + global intensity
            url = (
                f"http://{host}:{port}/config?"
                f"R-Time={r}&G-Time={g}&B-Time={b}"
                f"&INTENSITY={intensity}&INTENSITYviaWEB=1"
            )
        else:
            # Background only (no brightness change)
            url = (
                f"http://{host}:{port}/config?"
                f"R-Back={r}&G-Back={g}&B-Back={b}"
            )

        async with aiohttp.ClientSession() as session:
            await session.get(url)

        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        # Only meaningful for time (global intensity)
        host = self.entry.data["host"]
        port = self.entry.data["port"]

        url = (
            f"http://{host}:{port}/config?"
            f"INTENSITY=0&INTENSITYviaWEB=1"
        )

        async with aiohttp.ClientSession() as session:
            await session.get(url)

        await self.coordinator.async_request_refresh()
