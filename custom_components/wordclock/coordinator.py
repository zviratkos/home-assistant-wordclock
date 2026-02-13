import aiohttp
import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed

_LOGGER = logging.getLogger(__name__)

class WordClockCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, host, port, scan_interval):
        self.host = host
        self.port = port
        super().__init__(
            hass,
            _LOGGER,
            name="WordClock",
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self):
        url = f"http://{self.host}:{self.port}/status"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    text = await resp.text()
        except Exception as err:
            raise UpdateFailed(f"Error communicating: {err}")

        data = {}
        parts = text.strip().split()
        for item in parts:
            key, value = item.split("=")
            data[key] = int(value)

        return data
