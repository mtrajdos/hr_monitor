import asyncio
import scanner as sc
import data_capturer as dc
import connection as conn

HR_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
HR_MEASUREMENT_CHARACTERISTIC_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

async def main():
    device = await sc.find_device()
    connection = conn.Connection(device)
    
    hr_service = await connection.connect_to_hr_service(HR_SERVICE_UUID)

    if hr_service is not None:
        print(f"Connected to HR Service!")
    else:
        print("No HR Service found")
        return

# This is true only when the file is ran directly
if __name__ == "__main__":
    asyncio.run(main())
