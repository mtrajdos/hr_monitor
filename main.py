import asyncio
import plotly.express as px

from datetime import datetime
from collector import connection as conn
from collector import hr_listener as hl
from collector import scanner as sc
from scripts import query_handler as qh


async def main():
    hr_listener = None
    data_points = []
    query_handler = qh.QueryHandler()
    try:
        print("Welcome to the HR Monitor. Please choose an option:")
        print("1. Record new HR data")
        print("2. Query existing HR data")

        choice = input("Select an option: ")

        if choice == "1":
            print("Make sure to enable HR broadcast on your device")
            print("Attempting to connect in 10 seconds...")
            await asyncio.sleep(10)

            device = await sc.find_device()
            if device is None:
                return

            connection = conn.Connection(device)
            client = await connection.connect_to_client()
            if client is None:
                print("Could not connect")
                return

            hr_listener = hl.HRListener(client)
            data = await hr_listener.get_hr_data()
            print("Connected to HR Service!")

            while True:
                data = await hr_listener.get_hr_data()
                print(f"Reading: {data}")

        elif choice == "2":
            print(
                "Enter the start and end times for the query in the appropriate format, "
                "e.g. 22-Sep-26 14:53:21.029 (seconds are optional):"
            )
            try:
                start_time = input("Start time: ")
                end_time = input("End time: ")
                rows = query_handler.get_rows_between_times(start_time, end_time)
                print(f"Found {len(rows)} rows")

                for row in rows:
                    data_points.append([row[1].split(" ")[1], row[2]])

                x_times = [x[0] for x in data_points]
                y_hr = [x[1] for x in data_points]

                fig = px.line(x=x_times, y=y_hr, labels={"x": "Time", "y": "HR"})
                fig.update_xaxes(tickangle=45)
                fig.show()


            except Exception as e:
                print(f"Error: {e}")

        else:
            print("Invalid choice")
            return

    except asyncio.CancelledError:
        pass
    finally:
        if hr_listener is not None:
            await hr_listener.stop()
        print("Exiting...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
