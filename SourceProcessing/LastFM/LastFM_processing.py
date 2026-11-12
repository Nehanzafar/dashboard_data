import json

from dotenv import load_dotenv
import os
from SourceProcessing.BaseClass import SourceProcessing
from utils.request_handler import Request_handler
from utils.logger import logger


load_dotenv()
export_file_path = "SourceProcessing/exportedFiles/"

try:
    log = logger("LastFM Data Fetching")
except Exception as e:
    print(e)

class LastFMProcesser(SourceProcessing):
    def __init__(self):
        # get the enviroment variables
        self.api_key = os.getenv("LASTFM_API_KEY")
        # self.api_secret = os.environ.LASTFM_API_SECRET
        self.username = os.getenv("LASTFM_USERNAME")
        

        if not self.username:
            log.error("UserName not set!")

        if not self.api_key:
            log.error("You need an api key to use the api!")
            log.message("You need to make an api account to get the api key from ${url}",)


        # URL and Param
        self.base_url = "https://ws.audioscrobbler.com/2.0/"
        log.success("Client api initialized!")


    def fetch_data(self, parameters: dict):
        self.add_user_data(parameters)
        try:
            request = Request_handler(self.base_url)
            data = request.GET( parameters)
            # request.validate(data)
            log.success(f"Status_Code: {data.status_code}\nSUCCESS!")
            log.success("The data has been successfully been recieved")
            return data.json()
        except Exception as e:
            log.error(e)
        # store the data in a json

    # not using this anymore
    def store_data_json(self, data):

        path = export_file_path + next(iter(data)) + ".json"
        print(path)
        log.loading("Storing in json")
        with open(path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        log.success(f"The data is stored in the json file at {path}")

    # Takes the paramter list and adds the api key to it and the fixed username
    def add_user_data(self, parameters: dict):
        parameters["user"] = self.username
        parameters["api_key"] = self.api_key

        return parameters

