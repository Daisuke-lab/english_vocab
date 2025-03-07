class Vocabulary {
  constructor(row) {
    this.row = row
  }

  hasDefinitions() {
    var cell = row.getCell(1, 3)
    return cells.getValue() != ""
  }

  setDefinitions(definitions) {
    defintionStr = ""
    for (let i=0; i < definitions.length; i++) {
      definitionStr += `・${definition}\n`
    }
    var cell = row.getCell(1, 1)
    cell.setValue(value)
  }

  setExamples(examples) {

  }

  hasWord() {
    getWord() != ""
  }

  getWord() {
    var cell = row.getCell(1, 2)
    return cells.getValue()
  }

  




}
