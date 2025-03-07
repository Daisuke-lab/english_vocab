function myFunction() {
  const spreadSheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheets = spreadSheet.getSheets()
  const range = getRow(sheets[0].getSheetId, 1)
  Logger(range.getCell(1, 1).getValue())
  // for (var i = 0; i < sheets.length; i++) {
  //   sheets[0].getSheetId
  // }

}

function getRow(sheetId, count) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetById(sheetId)
  firstRowIndex = 8
  currentIndex = firstRowIndex + count
  return sheet.getRange(currentIndex, 0, currentIndex, sheet.getColumnWidth())
}


function fetchDefinition(word) {
    // API URL
    let url = `https://dictionary.cambridge.org/dictionary/english/${word}`;
    url = url.replace(" ", "%20")

    // Fetch data from API
    const headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    const  response = UrlFetchApp.fetch(url, headers);
    const data = JSON.parse(response.getContentText());
    return data
}