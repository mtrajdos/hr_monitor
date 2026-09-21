from bleak import BleakScanner

async def scan_for_devices():
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

        print(f"Found device: \nName: {name}")

        if name == "Forerunner 55":
            return device