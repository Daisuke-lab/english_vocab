from managers.sheet_manager import SheetManager
from managers.gemini_manager import GeminiManager
class Main:
    def main():
        sheet_manager = SheetManager()
        gemini_manager = GeminiManager()
        sheets = sheet_manager.get_sheets()
        for sheet in sheets:
            unchecked_words = sheet.get_unchecked_words()
            for word in unchecked_words:
                print(word)
                output = gemini_manager.search_word(word.value)
                print(output)
                sheet.insert_definitions(word, output["definitions"])
                sheet.insert_examples(word, output["examples"])


if __name__ == "__main__":
    Main.main()