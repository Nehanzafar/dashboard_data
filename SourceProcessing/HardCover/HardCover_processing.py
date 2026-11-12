import json

from dotenv import load_dotenv
import os
from SourceProcessing.BaseClass import SourceProcessing
from utils.request_handler import Request_handler
from utils.logger import logger


load_dotenv()
export_file_path = "SourceProcessing/exportedFiles/"
log = logger("HardCover Data Fetching")


class HardCoverProcessor(SourceProcessing):
    def __init__(self):
        # get the enviroment variables
        self.api_key = os.getenv("HARDCOVER_API_KEY")
        # self.api_secret = os.environ.HARDCOVER_API_SECRET
        self.username = os.getenv("HARDCOVER_USERNAME")
        

        if not self.username:
            log.error("UserName not set!")

        if not self.api_key:
            log.error("You need an api key to use the api!")
            log.message("You need to make an api account to get the api key from ${url}",)


        # URL and Param
        self.base_url = "https://api.hardcover.app/v1/graphql"

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        log.success("Client api initialized!")


    def fetch_data(self, query: str):
        try:
            request = Request_handler(self.base_url, self.headers)
            data = request.POST(query)
            # request.validate(data)
            log.success(f"Status_Code: {data.status_code}\nSUCCESS!")
            log.success("The data has been successfully been recieved")
            return data.json()
        except Exception as e:
            log.error(e)
        # store the data in a json

    # Takes the paramter list and adds the api key to it and the fixed username
    def add_user_data(self, parameters: dict):
        parameters["user"] = self.username
        parameters["api_key"] = self.api_key

        return parameters

