class Sheet:
    def __init__(self, ws):
        self.ws = ws

    def get_words(self):
        columns_num = 5
        first_row_index = 8
        first_column_index = 2
        for i in range(1000):
            current_index = first_row_index
            #row = ws.range(current_index, first_column_index, current_index, columns_num)
            word = self.ws.cell(current_index, first_column_index)
            yield word
                

    def has_definition(self, word)
        i = word.row
        j = word.col + 1
        return self.ws.cell(i, j).value != ""

    def get_unchecked_words(self):
        words = self.get_words()
        unchecked_words = []
        while True:
            words = next(words)
            if word.value.strip() == "":
                break
            if self.has_definition(word):
                continue
            unchecked_words.append(word)
        return unchecked_words

        
    def insert_definitions(self, word, definitions):
        i = word.row
        j = word.col + 1
        text = StringUtil.convert_list_to_string(definitions)
        cell = self.ws.cell(i, j)
        cell.value = text

    def insert_examples(self, word, examples):
        i = word.row
        j = word.col + 2
        text = StringUtil.convert_list_to_string(example)
        cell = self.ws.cell(i, j)
        cell.value = text