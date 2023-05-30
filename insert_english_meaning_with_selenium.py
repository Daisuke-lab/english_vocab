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
    


    def connect_to_webdriver(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())



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

        
        info = {"name": name, "definitions": definitions, "examples": examples, "url":current_url}

        return info


    def main(self):
        try:
            self.connect_to_webdriver()
            super.main()
        finally:
            self.driver.close()

    

if __name__ == "__main__":
    instance = InsertEnglishMeaning()
    instance()
                  
        