import asyncio

HR_MEASUREMENT_CHARACTERISTIC_UUID = "00002a37-0000-1000-8000-00805f9b34fb"


def parse_hr_data(data: bytearray) -> int:
    flags = data[0]
    if flags & 0x01:
        return int.from_bytes(data[1:3], byteorder="little")
    return data[1]


class HRListener:
    def __init__(self, client):
        self.client = client  # the BLE connection (the pipe)
        self.data = None      # filled later, when the watch pushes bytes
        self._got_reading = asyncio.Event() # Flag to indicate that a reading has arrived

    async def get_hr_data(self) -> int:
        # Reset the "reading arrived" flag
        self._got_reading.clear()

        # Subscribe: tell Bleak to call _on_hr when the watch pushes data
        #     (this does NOT read HR yet — it only registers the listener)
        await self.client.start_notify(
            HR_MEASUREMENT_CHARACTERISTIC_UUID,
            self._on_hr,
        )

        # Wait until the data reading arrives
        await self._got_reading.wait()

        # Callback on_hr has populated the data, so we can return it
        return self.data

    # ------------------------------------------------------------------
    # LINE B — Bleak calls this later.
    # ------------------------------------------------------------------
    def _on_hr(self, sender, data: bytearray):
        # BWatch sent `data` over BLE; Bleak hands it to us here
        # Parse bytes → BPM and store
        self.data = parse_hr_data(data)
        # Flip the flag so A3 can continue → A4
        self._got_reading.set()
