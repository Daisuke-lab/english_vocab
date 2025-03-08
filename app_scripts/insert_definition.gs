function myFunction() {
  const spreadSheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheets = spreadSheet.getSheets()
  const range = getRow(sheets[0].getSheetId(), 1)
  vocab = new Vocabulary(range)
  Logger.log(vocab.getWord())
  Logger.log(range.getCell(1, 2).getValue())
  vocab = new Vocabulary(range)
  if (vocab.hasWord()) {
    fetchDefinition(vocab.getWord())
  }
  // for (var i = 0; i < sheets.length; i++) {
  // }

}


function getRow(sheetId, count) {
  Logger.log(sheetId)
  Logger.log(count)
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetById(sheetId)
  firstRowIndex = 8
  currentIndex = firstRowIndex + count
  Logger.log(sheet.getMaxColumns())
  return sheet.getRange(currentIndex, 1, currentIndex, sheet.getMaxColumns())
}


function fetchDefinition(word) {
    // API URL
    let url = `https://dictionary.cambridge.org/dictionary/english/${word}`;
    url = url.replace(" ", "%20")

    // Fetch data from API
    const headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    const response = UrlFetchApp.fetch(url, headers);
    Logger.log(response.getContentText())
    const data = JSON.parse(response.getContentText());
    Logger.log(data)
    return data
}