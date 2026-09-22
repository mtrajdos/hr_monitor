# HR Monitor

Prototype for reading heart-rate data from a Garmin Forerunner 55 over Bluetooth Low Energy (BLE).

## Current status

The app **scans** for a Forerunner 55, **connects** over BLE, then **subscribes** to the standard Heart Rate Measurement characteristic and prints BPM as notifications arrive.

| File | Role |
| --- | --- |
| `main.py` | Entry point: scan → connect → listen for HR readings in a loop |
| `scanner.py` | BLE discovery via [Bleak](https://github.com/hbldh/bleak); returns the Forerunner 55 when found |
| `connection.py` | Wraps `BleakClient`; connects to the scanned device |
| `hr_listener.py` | Subscribes with `start_notify`, parses HR Measurement bytes into BPM |

Heart rate is delivered as **GATT notifications**, not a one-shot read. Flow in `hr_listener.py`:

1. `start_notify` — register a callback for characteristic `00002a37-…`
2. Wait until the watch pushes a packet
3. Callback receives a `bytearray`, parses flags + BPM, unblocks the waiter
4. Return the BPM (`int`)

## Roadmap

Step-by-step plan (persist → SQL windows → API → graphs → Docker/CI → hosting): see **[ROADMAP.md](ROADMAP.md)**.

## Direction

Later, this is meant to become a **full-stack app** that shows **live** heart-rate (and related) data on screen.

Live updates will only be as good as the hardware and firmware allow:

- **TP-Link Bluetooth 5.4 USB adapter** — radio range, Windows BLE stack, and how quickly advertisements and GATT notifications arrive
- **Garmin Forerunner 55** — which BLE services it exposes, and whether heart-rate streams reliably to third-party clients (Garmin watches often limit this compared with a dedicated chest strap)

If the watch does not stream HR over BLE, the UI can still be built, but the live feed will be limited to whatever the device exposes.

## Hardware

| Role | Device |
| --- | --- |
| BLE adapter | TP-Link Bluetooth 5.4 USB adapter |
| Watch | Garmin Forerunner 55 |

## Run

```powershell
python -m pip install bleak
python main.py
```

Keep the USB adapter plugged in and Bluetooth enabled. Wear the watch (or otherwise keep HR sensing active) so notifications can arrive. The scan lasts up to 10 seconds; after connect, the app prints the first reading, then keeps printing as new notifications come in. Stop with `Ctrl+C`.
