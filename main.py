import asyncio
import scanner as sc

async def main():
    await sc.scan_for_devices()

# This is true only when the file is ran directly
if __name__ == "__main__":
    asyncio.run(main())
