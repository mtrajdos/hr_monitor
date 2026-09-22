from bleak import BleakScanner


async def find_device():
    print("Scanning for Bluetooth devices for 10 seconds...")

    results = await BleakScanner.discover(
        timeout=10.0,
        return_adv=True,
    )

    if not results:
        print("No devices found. Check that Bluetooth is enabled.")
        return

    for device, advertisement in results.values():
        name = advertisement.local_name or device.name or "(unnamed)"

        print(f"Found device: \nName: {name}")

        if name == "Forerunner 55":
            print("Forerunner 55 found!")
            return device
