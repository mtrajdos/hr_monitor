# Heart-rate reading is paused while we establish a persistent PC link.
# Uncomment / finish this later once the connection stays up reliably.

# def capture_and_display_data(client, HR_SERVICE_UUID):
#     print("Capturing data...")
#     while client.is_connected:
#         print("Heart Rate: " +
#         str(client.services.get_characteristic(HR_SERVICE_UUID).read()))
