import uuid
import datetime
from collector import storage_handler as storage

storage = storage.StorageHandler()

class Session:
    def __init__(self):
        self.session_id = None
        self.session_start_time = None
        self.session_end_time = None

    def start(self):
        self.session_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().strftime("%d-%b-%y %H:%M:%S.%f")[:-3]
        self.session_start_time = timestamp
        storage.set_row(self.session_id, self.session_start_time, None)

    def add_row(self, data):
        timestamp = datetime.datetime.now().strftime("%d-%b-%y %H:%M:%S.%f")[:-3]
        storage.set_row(self.session_id, timestamp, data)

    def stop_and_save(self):
        timestamp = datetime.datetime.now().strftime("%d-%b-%y %H:%M:%S.%f")[:-3]
        self.session_end_time = timestamp
        storage.set_row(self.session_id, self.session_end_time, None)

