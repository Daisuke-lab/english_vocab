from managers.sheet_manager import SheetManager
from managers.gemini_manager import GeminiManager

class Debug:

    def main():
        Debug.test_sheet_manager()

    def test_gemini_manager():
        print(GeminiManager().search_word("indulge"))
        
    def test_sheet_manager():
        manager = SheetManager()
        sheet = manager.get_sheets()[0]
        word = sheet.get_unchecked_words()[0]
        sheet.insert_definitions(word, ["test"])
        sheet.insert_examples(word, ["test"])
        sheet.insert_definitions(word, [])


if __name__ == "__main__":
    Debug.main()