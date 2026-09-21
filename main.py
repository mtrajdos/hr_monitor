import asyncio
import scanner as sc
from bleak import BleakClient

async def main():
    device = await sc.scan_for_devices()

    if device is not None:
        print(f"Device found! Connecting to {device}...")
        async with BleakClient(device.address) as client:
            print("Connected: " + str(client.is_connected))
    else:
        print("No device found")

# This is true only when the file is ran directly
if __name__ == "__main__":
    asyncio.run(main())
