import asyncio
import device_scanner as ds

async def main():
    await ds.scan_for_devices()

# This is true only when the file is ran directly
if __name__ == "__main__":
    asyncio.run(main())
