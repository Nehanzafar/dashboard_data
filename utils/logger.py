from datetime import datetime
import os
from colorama import Fore


class logger:
    def __init__(self, process: str = ""):
        self.curDir = os.getcwd()
        self.path = "log/" + os.path.basename(self.curDir) + ".txt"
        self.process = process
        
    def success(self, message):
        print(Fore.WHITE + "[", end=" ")
        print(Fore.GREEN + f"DEBUG", end="")
        print(Fore.WHITE + " ]")
        print(Fore.WHITE + f"{self.process}")
        # print(f"[DEBUG] {self.curDir}")

        print(Fore.WHITE + f"{message}")

    def error(self, message):
        print(Fore.WHITE + "[", end=" ")
        print(Fore.RED + f"DEBUG", end="")
        print(Fore.WHITE + " ]")
        print(Fore.WHITE + f"{self.process}")
        # print(f"[DEBUG] {self.curDir}")
        print(Fore.WHITE + f" {message}")
        # self.log_error(message)

    def message(self, message):
        print(Fore.YELLOW + f"[DEBUG] {self.process}")
        print(f" {message}")

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
