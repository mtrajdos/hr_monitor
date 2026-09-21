# asyncio lets us run code that waits (e.g. for Bluetooth replies) without freezing the whole program
import asyncio

# BleakScanner is the class that looks for nearby Bluetooth Low Energy (BLE) devices
from bleak import BleakScanner


# async means this function can pause and wait for Bluetooth results instead of blocking
async def main():
    # Tell the user a scan is starting and how long it will take
    print("Scanning for Bluetooth devices for 10 seconds...")

    # Wait until the scanner finishes, then store whatever devices it found
    results = await BleakScanner.discover(
        timeout=10.0,  # listen for advertisements for 10 seconds
        return_adv=True,  # also return advertisement data (name, signal, services), not just the device
    )

    # results is empty if nothing nearby advertised during the scan
    if not results:
        # Hint the most common cause: Bluetooth radio off or no permission
        print("No devices found. Check that Bluetooth is enabled.")
        # Stop here; there is nothing to print in the loop below
        return

    # Each result is a (device, advertisement) pair; .values() walks those pairs
    for device, advertisement in results.values():
        # Prefer the name from the advertisement, then the device object, else a placeholder
        name = advertisement.local_name or device.name or "(unnamed)"

        # Blank line plus the human-readable name of this device
        print(f"\nName: {name}")
        # MAC address (Windows) or UUID (some OS Bluetooth stacks) that identifies this radio
        print(f"Address: {device.address}")
        # RSSI is signal strength in dBm; closer to 0 usually means stronger / nearer
        print(f"Signal: {advertisement.rssi} dBm")
        # UUIDs the device advertised; heart-rate monitors typically include 0000180d-...
        print(f"Advertised services: {advertisement.service_uuids}")


# This is true only when you run this file directly (python scan.py), not when another file imports it
if __name__ == "__main__":
    # Start the asyncio event loop and run main() until the scan and printing are done
    asyncio.run(main())
