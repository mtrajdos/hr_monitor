HR_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
HR_MEASUREMENT_CHARACTERISTIC_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

class HRListener:
    def __init__(self, client):
        self.client = client
        self.data = None

    async def get_hr_data(self):
        self.data = data = await self.client.read_gatt_char(HR_MEASUREMENT_CHARACTERISTIC_UUID)
        return self.data
