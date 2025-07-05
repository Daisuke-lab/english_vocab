from oauth2client.service_account import ServiceAccountCredentials
import gspread

class SheetManager:
    def __init__(self):
        current_dir = self.get_curr_dir()
        load_dotenv(os.path.join(curr_dir, ".env"))
        url = os.environ.get("SPREADSHEET_URL")
        self.workbook = self.connect_to_spreadsheet(url)

    def get_curr_dir(self):
        # Pyinstaller exe
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        # general python
        elif __file__:
            application_path = os.path.dirname(__file__)
        return application_path


    def connect_to_spreadsheet(self):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        path = r'C:\envs\english_vocab\google-service-account.json'
        credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
        gc = gspread.authorize(credentials)
        key = self.url.split("/")[5]
        workbook = gc.open_by_key(key)
        return workbook

    def get_sheets():
        sheets = []
        worksheets = self.workbook.worksheets()
        sheets = [Sheet(ws) for ws in worksheets]
        return sheets