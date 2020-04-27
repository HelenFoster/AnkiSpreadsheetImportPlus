#!/usr/bin/sh

# Run this file from the directory it's in.
# Creates spreadsheet_import_plus.ankiaddon (preventing overwriting).

if [ -e "spreadsheet_import_plus.ankiaddon" ]
then
  echo "Please rename or delete spreadsheet_import_plus.ankiaddon"
  exit
fi

(cd spreadsheet_import_plus && zip -r ../spreadsheet_import_plus.ankiaddon . --exclude \*.pyc \*pycache\* meta.json)
