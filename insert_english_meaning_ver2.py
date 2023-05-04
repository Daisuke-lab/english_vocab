from site import check_enableusersite
import requests
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import bs4
from time import sleep 
class InsertEnglishMeaning:
    
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

    def already_checked(self, row):
        cells = row
        return cells[3].value != ""

    def search_meaning(self, row):
        cells = row
        name = cells[0].value
        url = f"https://dictionary.cambridge.org/dictionary/english/{name}"
        self.driver.get(url)
        soup = bs4.BeautifulSoup(self.driver.page_source, 'html.parser')
        name = soup.select('.di-title')[0].text if len(soup.select('.di-title')) > 0 else "Not Found"
        row_definitions = soup.select('.def')
        row_examples = soup.select('.examp')
        current_url = self.driver.current_url
        examples = []
        definitions = []
        for index, row_example in enumerate(row_examples):
            example = row_example.text
            examples.append(example)
            if index == 5:
                break

        for index, row_definition in enumerate(row_definitions):
            definition = row_definition.text
            definition = definition.replace(':', "")
            definitions.append(definition)



        return name, definitions, examples, current_url

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
        print("has word", cells[0].value)
        return cells[0].value != ""

    def ws_already_checked(self, ws):
        value = ws.acell('A3').value
        return value == "TRUE"

    def test(self):
        self.already_checked(self.workbook.worksheets()[0])
        
        

    def __call__(self):
        try:
            for ws in self.workbook.worksheets():
                count = -1
                checked_every_word = self.ws_already_checked(ws)
                while checked_every_word == False:
                    count += 1
                    sleep(1)
                    row = self.get_row(ws, count)
                    if self.already_checked(row) == False:
                        if self.has_word(row):
                            name, definitions, examples, url = self.search_meaning(row)
                            info = {"name": name, "definitions": definitions, "examples": examples, "url":url}
                            if definitions != []:
                                self.insert_info(ws, row, info)
                        else:
                            print("you have checked every word!!")
                            checked_every_word = True
        finally:
            self.driver.close()

    

if __name__ == "__main__":
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1QtdcbvmGHlgA-3E2lSHj9CNLhGKmQDBhvO5AoVSivtU/edit#gid=1577131084"
    instance = InsertEnglishMeaning(spreadsheet_url)
    instance()
                  
        