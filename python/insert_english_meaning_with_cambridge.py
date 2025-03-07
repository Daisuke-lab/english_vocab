
import requests
from bs4 import BeautifulSoup as bs4

from common import Common


class EnglishMeaningInserter(Common):

    def search_meaning(self, row):
        cells = row
        name = cells[0].value
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
        url = f"https://dictionary.cambridge.org/dictionary/english/{name}"
        url = url.replace(" ", "%20")
        res = requests.get(url, headers=headers)
        soup = bs4(res.text, 'html.parser')
        row_definitions = soup.find_all("div", class_="def ddef_d db")
        row_examples = soup.find_all("div", class_="examp dexamp")
        examples = []
        definitions = []
        for index, row_example in enumerate(row_examples):
            example = row_example.text
            examples.append(example)
            if index == 2:
                break

        for index, row_definition in enumerate(row_definitions):
            definitions.append(row_definition.text)
            if index == 1:
                break
            
        info = {"name": name, "definitions": definitions, "examples": examples, "url":url}
        return info

if __name__ == "__main__":
    inserter = EnglishMeaningInserter()
    inserter.main()