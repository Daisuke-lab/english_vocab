
from site import check_enableusersite
import requests
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import bs4
from time import sleep 
from selenium.webdriver.common.by import By
import random


class PronouceSpeaker():
    def __init__(self, url):
        self.url = url
        self.connect_to_spreadsheet()
        self.connect_to_webdriver()
        self.rows = []


    def connect_to_spreadsheet(self):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        path = r'C:\Users\daisu\Periodical\google-service-account.json'
        credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
        gc = gspread.authorize(credentials)
        key = self.url.split("/")[5]
        self.workbook = gc.open_by_key(key)


    def connect_to_webdriver(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def get_row(self, ws, count):
        columns_num = 5
        first_row_index = 8
        first_column_index = 2
        current_index = first_row_index + count
        return ws.range(current_index, first_column_index, current_index, columns_num)


    def has_pronunciation(self, row):
        return "cambridge" in row[3].value

    def has_word(self, row):
        cells = row
        return cells[0].value != ""

    def pronounce(self, row):
        try:
            url = row[3].value
            self.driver.get(url)
            sleep(2)
            self.driver.find_element(By.CLASS_NAME, 'daud').click()

        except Exception as e:
            pass
        finally:
            sleep(2)
        

    def main(self):
        try:
            ws = self.workbook.worksheets()[2]
            checked_every_word = False
            count = 0
            while checked_every_word == False:
                count += 1
                sleep(1)
                row = self.get_row(ws, count)
                if self.has_pronunciation(row) and self.has_word(row):
                    self.pronounce(row)
                elif self.has_word(row):
                    pass
                else:
                    checked_every_word = True
        finally:
            self.driver.close()

    def random(self):
        try:
            ws = self.workbook.worksheets()[6]
            nums = [i for i in range(0, 101 - 8)]
            while len(nums) > 0:
                random_num = random.choice(nums)
                nums.remove(random_num)
                sleep(1)
                row = self.get_row(ws, random_num)
                if self.has_pronunciation(row) and self.has_word(row):
                    self.pronounce(row)

        finally:
            self.driver.close()
        



if __name__ == "__main__":
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1KeDraCw1FABNJhah-CXukKyr_q6nj0QVG-JtabZlXoA/edit#gid=1937968625"
    pronounce_speaker = PronouceSpeaker(spreadsheet_url)
    pronounce_speaker.random()
