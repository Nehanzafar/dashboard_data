import datetime as datetime
import time

import requests

from utils.logger import logger
from urllib.parse import urlsplit


class Request_handler:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.log = logger()
        self.attempt = 1
        self.curParameters = {}

    def GET(self, parameters: dict) -> requests.Response:
        try:
            self.curParameters = parameters
            data = requests.api.get(self.base_url, parameters, timeout=10)

            data.raise_for_status()

            return data
        except requests.exceptions.HTTPError as http_err:
            # Catches 4xx and 5xx status codes
            status_code = http_err.response.status_code
            self.log.message(f"Status code: {status_code}")

            log_message = f"Status Code: {status_code} Endpoint: {urlsplit(http_err.response.url).query} \nResponse: {http_err.response.text} \nFailed URL: {http_err.response.url}"
            if status_code == 400:
                self.log.error(log_message)
            elif status_code == 401:
                # Implement credential refresh on api that require authentication
                pass                   
            elif status_code == 403:
                self.log.error("FORBIDDEN")
                self.log.error(log_message)
                # TODO
                # implement a alert menu
                self.log.alert()
            elif status_code == 404:
                self.log.error("NOT FOUND")
                self.log.error(log_message)
                self.log.alert() #TODO complete this
            elif status_code == 429:
                self.log.error("TOO MANY TRIES")
                self.log.error(log_message)

                data = self.backoff()
                if data is not None:
                    return data
            elif status_code == 500:
                self.log.error("API CRASHED INTERNALLY")
                self.log.error(log_message)

                data = self.backoff()
                if data is not None:
                    return data
            elif status_code == 502:
                self.log.error("UPSTREAM SERVER ERROR")
                self.log.error(log_message)

                data = self.backoff()
                if data is not None:
                    return data
            elif status_code == 503:
                self.log.error("API TEMPORARILY UNAVAILABLE")
                self.log.error(log_message)


                data = self.backoff()
                if data is not None:
                    return data

            elif status_code == 504:
                self.log.error("API TOOK TOO LONG")
                self.log.error(log_message)

                data = self.backoff()
                if data is not None:
                    return data
            
    

        except requests.exceptions.ConnectionError as conn_err:
            # Catches network drops, DNS failures, or refused connections
            self.log.error(f"Connection error occurred: {conn_err}")
            data = self.backoff()
            if data is not None:
                return data
            
        except requests.exceptions.Timeout as time_err:
            # Catches requests that exceeded the timeout limit
            self.log.error(f"Timeout error occurred: {time_err}")

            data = self.backoff()
            if data is not None:
                return data

            
        except requests.exceptions.RequestException as general_err:
            # Catch-all for any other unexpected requests-related issues
            self.log.error(f"An unexpected error occurred: {general_err}")
            data = self.backoff()
            if data is not None:
                return data

    def abort(self):
        self.log.error("ABORTED!")

    def backoff(self):
        self.log.loading("Retrying")
        self.log.message(f"Attempt: {self.attempt}")
        if self.attempt == 5:
            raise requests.exceptions.Timeout("Maximum number of retries reached!")
        time.sleep(self.attempt * 2)
        self.attempt += 1

        return self.GET(self.curParameters)

