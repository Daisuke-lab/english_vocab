
import requests
from bs4 import BeautifulSoup as bs4

from common import Common


class EnglishMeaningInserter(Common):

    def search_meaning(self, row):
        cells = row
        name = cells[0].value
        url = f"https://www.merriam-webster.com/dictionary/{name}"
        url = url.replace(" ", "%20")
        res = requests.get(url)
        soup = bs4(res.text, 'html.parser')
        row_definitions = soup.find_all("a", class_="fb share-link")
        row_examples = soup.find_all("span", class_="t has-aq")
        examples = []
        definitions = []
        for index, row_example in enumerate(row_examples):
            example = row_example.text
            examples.append(example)
            if index == 5:
                break

        for index, row_definition in enumerate(row_definitions):
            _definitions = row_definition.attrs['data-share-description'].replace("… See the full definition", "").split(";")
            definitions.extend(_definitions)
        info = {"name": name, "definitions": definitions, "examples": examples, "url":url}
        return info

if __name__ == "__main__":
    inserter = EnglishMeaningInserter()
    inserter.main()