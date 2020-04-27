# New code copyright (C) 2020  Helen Foster
#
# Based on various Anki code in pylib/anki/importing
# Copyright: Ankitects Pty Ltd and contributors
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import openpyxl
import html
import markdown
from itertools import islice, takewhile
from typing import List

from anki.collection import _Collection
from anki.importing.noteimp import ForeignNote, NoteImporter

def cellIsEmpty(cell):
    return cell.value is None or cell.value == ""

def rowIsEmpty(row):
    return all([cellIsEmpty(cell) for cell in row])

def untilEmpty(row):
    return takewhile(lambda cell: not cellIsEmpty(cell), row)

class SpreadsheetImporter(NoteImporter):
    
    needMapper = True
    needDelimiter = False
    
    def __init__(self, col: _Collection, file: str) -> None:
        NoteImporter.__init__(self, col, file)
        self.opened = False
        self.workbook = None
        self.worksheet = None
        self.tagsToAdd: List[str] = []
        self.numFields = 0
    
    def foreignNotes(self) -> List[ForeignNote]:
        md = markdown.Markdown()
        self.open()
        self.log = []
        notes = []
        if not self.allowHTML:
            raise Exception('"Allow HTML in fields" must be checked. Aborting.')
        rows = islice(self.worksheet.rows, 4, None)
        for row in rows:
            note = ForeignNote()
            for i in range(self.numFields):
                if i >= len(row) or row[i].value is None:
                    item = ""
                else:
                    item = str(row[i].value)
                if self.fieldTypes[i] == "text":
                    item = html.escape(item, quote=False)
                    item = item.strip()
                    item = item.replace("\n", "<br>")
                elif self.fieldTypes[i] == "markdown":
                    item = md.reset().convert(item)
                else:
                    #html
                    pass
                note.fields.append(item)
            note.tags.extend(self.tagsToAdd)
            notes.append(note)
        self.workbook.close()
        self.opened = False
        return notes
    
    def open(self) -> None:
        "Open file and ensure it's in the right format."
        magic = "SpreadsheetImportPlus v1"
        allowedTypes = ["text", "html", "markdown"]
        if not self.opened:
            self.workbook = openpyxl.load_workbook(self.file, read_only=True, data_only=True)
            for worksheet in self.workbook:
                if worksheet["A1"].value == magic:
                    self.worksheet = worksheet
            if not self.worksheet:
                raise Exception(f'No sheet found with A1="{magic}"')
            
            def fieldHelp(rowname):
                return [cell.value for cell in untilEmpty(self.worksheet[rowname])]
            fieldNames = fieldHelp("2")
            fieldTypes = fieldHelp("3")
            
            if len(fieldNames) < 1:
                raise Exception("No fields found")
            if len(fieldNames) != len(fieldTypes):
                raise Exception(f"Found {len(fieldNames)} fields but {len(fieldTypes)} field types")
            for fieldType in fieldTypes:
                if fieldType not in allowedTypes:
                    raise Exception(f'Found field type "{fieldType}"; must be one of ' + str(allowedTypes))
            if not rowIsEmpty(self.worksheet["4"]):
                raise Exception("Row 4 must be blank")
            
            self.fieldNames = fieldNames
            self.fieldTypes = fieldTypes
            self.numFields = len(fieldNames)
            self.opened = True
    
    def fields(self) -> int:
        "Number of fields."
        self.open()
        return self.numFields
    
    def initMapping(self) -> None:
        flds = [f["name"] for f in self.model["flds"]] + ["_tags"]
        self.mapping = []
        for i in range(self.fields()):
            if self.fieldNames[i] in flds:
                self.mapping.append(self.fieldNames[i])
            else:
                self.mapping.append(None)
