from bleak import BleakClient


class Connection:
    def __init__(self, device):
        self.connected = False
        self.device = device
        self.client = None

    async def connect_to_client(self):
        print(f"Connecting to device: {self.device.name}")
        self.client = BleakClient(self.device)
        await self.client.connect()
        if self.client.is_connected:
            self.connected = True
            return self.client
        return None
