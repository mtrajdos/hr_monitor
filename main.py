import asyncio

from collector import connection as conn
from collector import hr_listener as hl
from collector import scanner as sc


async def main():
    device = await sc.find_device()
    if device is None:
        return

    connection = conn.Connection(device)
    client = await connection.connect_to_client()
    if client is None:
        print("Could not connect")
        return

    hr_listener = hl.HRListener(client)
    try:
        data = await hr_listener.get_hr_data()
        print("Connected to HR Service!")
        print(f"First reading: {data}")

        while True:
            data = await hr_listener.get_hr_data()
            print(f"Reading: {data}")
    except asyncio.CancelledError:
        pass
    finally:
        await hr_listener.stop()
        print("Exiting...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
