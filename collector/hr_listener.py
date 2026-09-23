import asyncio
import datetime
from collector import session as se
from collector import storage_handler as storage

HR_MEASUREMENT_CHARACTERISTIC_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
session = se.Session()

def parse_hr_data(data: bytearray) -> int:
    flags = data[0]
    if flags & 0x01:
        return int.from_bytes(data[1:3], byteorder="little")
    return data[1]


class HRListener:
    def __init__(self, client):
        self.client = client
        self.data = None
        self._got_reading = asyncio.Event()
        self._subscribed = False

    async def get_hr_data(self) -> int:
        self._got_reading.clear()

        if not self._subscribed:
            await self.client.start_notify(
                HR_MEASUREMENT_CHARACTERISTIC_UUID,
                self._on_hr,
            )
            self._subscribed = True
            session.start()

        await self._got_reading.wait()
        session.add_row(self.data)
        return self.data

    def _on_hr(self, sender, data: bytearray):
        self.data = parse_hr_data(data)
        self._got_reading.set()

    async def stop(self):
        """Detach BLE notify + disconnect so Ctrl+C does not leave Bleak callbacks running."""
        if self._subscribed:
            try:
                await self.client.stop_notify(HR_MEASUREMENT_CHARACTERISTIC_UUID)
            except Exception:
                pass
            self._subscribed = False
            session.stop_and_save()
        if self.client is not None and self.client.is_connected:
            try:
                await self.client.disconnect()
            except Exception:
                pass
