import sys
from pathlib import Path

import json
import sqlite3

import pandas as pd

from utils.logger import logger
ImportFilePath = "SourceProcessing/exportedFiles/"
exportFilePath = "ExportProcessing/exportedFiles/"

log = logger("Data Processing")

class processer:
    def __init__(self, JSONdata):
        self.data = JSONdata
        log.success("processer initalized")

    def process(self, transformer):
        data = transformer(self.data)
        self.dataProcessed = data

    def convert_to_csv(self):
        try:
            for data in self.dataProcessed:
                exportPath = exportFilePath + data.attrs['Name'] + "_" + data.attrs['type'] + ".csv"
                log.success("converted to a csv file!")
                data.to_csv(exportPath, index=False)
        except Exception as e:
            log.error("Error in converting to csv file!!")
            log.error(e)


    def convert_to_sql(self):
        try:
            log.success("json normalized")
            # Connect to SQLite database
            connection = sqlite3.connect(exportFilePath + "dashboard.db")
            log.success("connection established!")
            # DataFrame → SQL table
            for data in self.dataProcessed:
                data.to_sql(
                    data.attrs["Name"] + data.attrs["type"],
                    connection,
                    if_exists="append",
                    index=False
                )
                log.success(f"{data.attrs["Name"] + data.attrs["type"]} data stored in sql db")
            log.success("json converted to sql table!")

            connection.close()
            log.success("Connection closed sucessfullly")
            log.success("Converted Successfully to SQL DB")
        except Exception as e:
            log.error("Error in converting to sql table!!")
            log.error(e)

    def convert_to_excel(self):

        try:
            with pd.ExcelWriter(exportFilePath + self.dataProcessed[0].attrs["Name"] + ".xlsx") as writer:
                for data in self.dataProcessed:
                    data.to_excel(writer, sheet_name=data.attrs["Name"] + data.attrs['type'], index=False)
            log.success("Converted to excel file!")
        except Exception as e:
            log.error(e)
            log.error("Failed to convert to excel file!")
