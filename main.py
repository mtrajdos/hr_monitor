import asyncio
import scanner as sc
import data_capturer as dc
from bleak import BleakClient

HR_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
HR_MEASUREMENT_CHARACTERISTIC_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

async def main():
    device = await sc.scan_for_devices()

    if device is not None:
        print(f"Device found! Connecting to {device}...")
        async with BleakClient(device) as client:
            print("Connected: " + str(client.is_connected))
            for service in client.services:
                if HR_SERVICE_UUID == service.uuid:
                    hr_service = service
    else:
        print("No device found")

    if hr_service is not None:
        print(f"HR Service found! {hr_service}")

# This is true only when the file is ran directly
if __name__ == "__main__":
    asyncio.run(main())
