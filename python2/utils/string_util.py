class StringUtil:
    def convert_list_to_string(array):
        text = ""
        for string in array:
            text += f"・{string}\n"
        text = text[:-1]
        return text