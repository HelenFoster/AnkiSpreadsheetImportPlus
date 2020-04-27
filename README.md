# Spreadsheet Import Plus for Anki

## Use case

* You want to maintain the data for a deck in a spreadsheet (so the canonical version is in the spreadsheet, and the data within Anki is a copy).
* The nature of your data means that Anki's built-in CSV import requires too many steps or is too error-prone.

## Features

* Imports XLSX files directly.
* Auto-matches field names.
* Allows each field to be configured within the spreadsheet as text, HTML or markdown.

## Required layout

* The target sheet in the workbook must have "SpreadsheetImportPlus v1" in cell A1.
* The rest of row 1 must be empty.
* Row 2 contains the field names. Name these the same as the field names within Anki to allow auto-matching. The name "_tags" maps to the tags. Anything after the first empty cell will be ignored.
* Row 3 contains the field types:
    * "text" means that HTML characters will be escaped (like when using the built-in CSV import without allowing HTML).
    * "html" means the input will be used as-is.
    * "markdown" means the input will be interpreted as Python-flavored Markdown. HTML tags will be preserved.
* Row 4 must be empty.
* The remaining rows contain the data to import. Any data to the right of the header rows will be ignored. Empty rows will be ignored by Anki's "empty first field" rule.

## Importing

XLSX files can be imported using Anki's usual import menus. In the import dialog, "Allow HTML in fields" must be checked. The fields can be remapped here, but it would normally make more sense to name them correctly in the spreadsheet.

## Development

Requires `openpyxl`, `et_xmlfile` and `jdcal.py` in the `spreadsheet_import_plus/lib` folder. These names are symlinked to a venv which can be set up as follows (on systems where this works and assuming Python 3.7). From the root directory of this repo:

```
python3 -m venv libs_venv
source libs_venv/bin/activate
pip install "openpyxl==3.0.3"
```
