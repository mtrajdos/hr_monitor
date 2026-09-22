from bleak import BleakClient

class Connection:
    def __init__(self, device):
        self.connected = False
        self.connected_device = None
        self.client = BleakClient(device)

    async def connect_to_hr_service(self, HR_SERVICE_UUID):
        await self.client.connect()
        for service in self.client.services:
            if HR_SERVICE_UUID == service.uuid:
                hr_service = service
                return hr_service
        return None