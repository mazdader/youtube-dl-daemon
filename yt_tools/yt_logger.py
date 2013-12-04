from yt_tools import yt_db

class yt_Logger:

    def __init__(self):
        self.db = yt_db.yt_DB_my()

    def log(self, log_text):
        self.db.log(log_text)

