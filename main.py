import asyncio
import scanner as sc
import hr_listener as hl
import connection as conn

async def main():
    device = await sc.find_device()
    connection = conn.Connection(device)
    client = await connection.connect_to_client()
    hr_listener = hl.HRListener(client)
    data = await hr_listener.get_hr_data()

    if hr_listener is not None:
        print(f"Connected to HR Service!")
        print(f"First reading: {data}")

    else:
        print("No HR Service found")
        return

    while True:
        data = await hr_listener.get_hr_data()
        print(f"Reading: {data}")

# This is true only when the file is ran directly
if __name__ == "__main__":
    asyncio.run(main())
