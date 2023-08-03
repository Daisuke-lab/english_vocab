from site import check_enableusersite
import requests
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import bs4
import traceback
import os
from dotenv import load_dotenv
from time import sleep 
import sys

class Common():

    def __init__(self, url=None):
        if url is not None:
            self.url = url
        else:
            current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            load_dotenv(os.path.join(current_dir, ".env"))
            self.url = os.environ.get("SPREADSHEET_URL")
            print(self.url)
        self.connect_to_spreadsheet()
        self.rows = []



    def connect_to_spreadsheet(self):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        path = r'C:\workspace\envs\english_vocab\google-service-account.json'
        credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
        gc = gspread.authorize(credentials)
        key = self.url.split("/")[5]
        self.workbook = gc.open_by_key(key)
        self.ws =self.workbook.worksheets()[-1]


    def already_checked_word(self, row):
        cells = row
        return cells[1].value != ""
    
    def get_row(self, ws, count):
        columns_num = 5
        first_row_index = 8
        first_column_index = 2
        current_index = first_row_index + count
        return ws.range(current_index, first_column_index, current_index, columns_num)
    
    def insert_info(self, ws, row, info):
        cells = row
        cells[0].value = info["name"]
        definition_text = ""
        for definition in info["definitions"]:
            definition_text += f"・{definition}\n"
        
        definition_text = definition_text[:-1]
        cells[1].value = definition_text
        example_text = f"{cells[2].value}\n" if cells[2].value != "" else ""
        for example in info["examples"]:
            example_text += f"・{example}\n"
        example_text = example_text[:-1]
        cells[2].value = example_text

        cells[3].value = info["url"]
        ws.update_cells(cells)

    def has_word(self, row):
        cells = row
        return cells[0].value != ""
    

    def already_checked_page(self, ws):
        value = ws.acell('A3').value
        return value == "TRUE"
    
    def search_meaning(self, row):
        raise Exception("you should override this method")
    
    def main(self):
        try:
            for ws in self.workbook.worksheets():
                count = -1
                checked_every_word = self.already_checked_page(ws)
                while checked_every_word == False:
                    count += 1
                    sleep(1)
                    row = self.get_row(ws, count)
                    if self.has_word(row):
                        if self.already_checked_word(row) is False:
                            info = self.search_meaning(row)
                            self.insert_info(ws, row, info)
                    else:
                        print("you have checked every word!!")
                        checked_every_word = True
        except:
            print(traceback.format_exc())
        finally:
            input("終了するにはEnterを押してください。")
            