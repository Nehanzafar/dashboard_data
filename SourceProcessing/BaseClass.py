from abc import abstractmethod
import json

from dotenv import load_dotenv
import os
from utils.request_handler import Request_handler
from utils.logger import logger


load_dotenv()
export_file_path = "SourceProcessing/exportedFiles/"
log = logger("Base Class")


class SourceProcessing:

    @abstractmethod
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

    # Takes the paramter list and adds the api key to it and the fixed username
    @abstractmethod
    def add_user_data(self, parameters: dict):
        parameters["user"] = self.username
        parameters["api_key"] = self.api_key

        return parameters

        # not using this anymore
    def store_data_json(self, data):

        path = export_file_path + next(iter(data)) + ".json"
        print(path)
        log.loading("Storing in json")
        with open(path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        log.success(f"The data is stored in the json file at {path}")