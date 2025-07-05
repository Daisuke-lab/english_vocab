from time import sleep 
from utils.string_util import StringUtil

class Sheet:
    def __init__(self, ws):
        self.ws = ws

    def get_words(self):
        columns_num = 5
        first_row_index = 8
        first_column_index = 2
        for i in range(1000):
            current_index = first_row_index + i
            #row = ws.range(current_index, first_column_index, current_index, columns_num)
            word = self.ws.cell(current_index, first_column_index)
            yield word
                

    def has_definition(self, word):
        i = word.row
        j = word.col + 1
        cell = self.ws.cell(i, j)
        return cell.value and cell.value != ""

    def get_unchecked_words(self):
        words = self.get_words()
        unchecked_words = []
        while True:
            word = next(words)
            # ease access quota
            sleep(2)
            if word.value is None or word.value.strip() == "":
                break
            if self.has_definition(word):
                continue
            unchecked_words.append(word)
        return unchecked_words

        
    def insert_definitions(self, word, definitions):
        i = word.row
        j = word.col + 1
        text = StringUtil.convert_list_to_string(definitions)
        self.ws.update_cell(i, j, text)

    def insert_examples(self, word, examples):
        i = word.row
        j = word.col + 2
        text = f"{word.value}\n" if word.value != "" else ""
        text += StringUtil.convert_list_to_string(examples)
        
        self.ws.update_cell(i, j, text)

