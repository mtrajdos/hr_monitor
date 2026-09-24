import uuid
import datetime
from collector import storage_handler as storage

storage = storage.StorageHandler()

class Session:
    def __init__(self):
        self.session_id = str(uuid.uuid4())

    def write_hr_reading(self, data):
        timestamp = datetime.datetime.now().strftime("%d-%b-%y %H:%M:%S.%f")[:-3]
        storage.write_hr_reading_to_db(self.session_id, timestamp, data)

