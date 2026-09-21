import asyncio

# Class to scan for Bluetooth devices
from bleak import BleakScanner


async def main():
    print("Scanning for Bluetooth devices for 10 seconds...")

    # Wait until the scanner finishes, then store whatever devices it found
    results = await BleakScanner.discover(
        timeout=10.0,       # Time to listen for advertisements (10 seconds)
        return_adv=True,    # Return advertisement data (name, signal, services)
    )

    if not results:
        print("No devices found. Check that Bluetooth is enabled.")
        return

    # Iterate through result pairs
    for device, advertisement in results.values():
        # Prefer the name from the advertisement, then the device object, else a placeholder
        name = advertisement.local_name or device.name or "(unnamed)"

        print(f"\nName: {name}")

        # Identifying MAC Address or Windows UUID
        print(f"Address: {device.address}")
        # RSSI (Received Signal Strength Indicator) - Signal strength in dBm, closer to 0 means stronger/nearer
        print(f"Signal: {advertisement.rssi} dBm")
        # UUIDs the device advertised; heart-rate monitors typically include 0000180d-...
        print(f"Advertised services: {advertisement.service_uuids}")


# This is true only when the file is ran directly
if __name__ == "__main__":
    asyncio.run(main())
