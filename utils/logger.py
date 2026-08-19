from datetime import datetime
import os


class logger:
    def __init__(self):
        self.curDir = os.getcwd()
        self.path = "log/" + os.path.basename(self.curDir) + ".txt"
    def success(self, message):
        print(f"[DEBUG] {self.curDir}")
        print(f"[DEBUG] {message}")

    def error(self, message):
        print(f"[DEBUG] {self.curDir}")
        print(f"[DEBUG] {message}")
        # self.log_error(message)

    def message(self, message):
        print(f"[DEBUG] {message}")

    def loading(self, message):
        pass

    def alert(self):
        pass

    def log_error(self, message):

        datetimeNow = datetime.now()
        with(open(self.path, "a") as log_file):
            log_file.write(
                message
            )
            log_file.write(f"${datetimeNow} \n")
