from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os
import sys
from dotenv import load_dotenv
from entities.sheet import Sheet

class SheetManager:
    def __init__(self):
        curr_dir = self.get_curr_dir()
        load_dotenv(os.path.join(curr_dir, ".env"))
        url = os.environ.get("SPREADSHEET_URL")
        self.workbook = self.connect_to_spreadsheet(url)

    def get_curr_dir(self):
        # Pyinstaller exe
        if getattr(sys, 'frozen', False):
            curr_dir = os.path.dirname(sys.executable)
        # general python
        elif __file__:
            curr_dir = os.getcwd()
        return curr_dir


    def connect_to_spreadsheet(self, url):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        path = r'C:\envs\english_vocab\google-service-account.json'
        credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
        gc = gspread.authorize(credentials)
        key = url.split("/")[5]
        workbook = gc.open_by_key(key)
        return workbook

    def get_sheets(self):
        sheets = []
        worksheets = self.workbook.worksheets()
        sheets = [Sheet(ws) for ws in worksheets]
        return sheets

if __name__ == "__main__":
    manager = SheetManager()
    ws = manager.get_sheets()[0]
    sheet = Sheet(ws)
    word = sheet.get_unchecked_words()[0]
    sheet.insert_definitions(word, ["test"])
    sheet.insert_examples(word, ["test"])
    sheet.insert_definitions(word, [])
    sheet.insert_examples(word, [])
    