# HR Monitor

Prototype for reading heart-rate data from a Garmin Forerunner 55 over Bluetooth.

## Current status

The first version is a **Bluetooth connector** that scans for nearby BLE devices and stops when it finds a **Forerunner 55**.

| File | Role |
| --- | --- |
| `main.py` | Entry point; runs the async scan |
| `scanner.py` | BLE discovery via [Bleak](https://github.com/hbldh/bleak); prints devices and returns the Forerunner 55 when found |

The next step is connecting to the watch and reading the Heart Rate service when it is exposed.

## Direction

Later, this is meant to become a **full-stack app** that shows **live** heart-rate (and related) data on screen.

Live updates will only be as good as the hardware and firmware allow:

- **TP-Link Bluetooth 5.4 USB adapter** — radio range, Windows BLE stack, and how quickly advertisements and GATT notifications arrive
- **Garmin Forerunner 55** — which BLE services it actually broadcasts, and whether heart-rate can be parsed in real time (Garmin watches often limit third-party BLE HR compared with a dedicated chest strap)

If the watch does not stream HR over BLE, the UI will still be built, but the live feed will be limited to whatever the device exposes.

## Hardware

| Role | Device |
| --- | --- |
| BLE adapter | TP-Link Bluetooth 5.4 USB adapter |
| Watch | Garmin Forerunner 55 |

## Run the scanner

```powershell
python -m pip install bleak
python main.py
```

Keep the USB adapter plugged in and Bluetooth enabled. The scan lasts up to 10 seconds and exits early if a Forerunner 55 is found.
