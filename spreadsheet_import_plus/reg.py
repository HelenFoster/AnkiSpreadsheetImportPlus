# Copyright (C) 2020  Helen Foster
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Jan 2022 fixes for Anki 2.1.45 by CommanderPho and Arthur Milchior

import os
import sys
from importlib import reload

from aqt.utils import showText
from anki import importing

def register(again=False):
    """Register the new importer with Anki's importers."""
    if not again:
        # Only on first time should we backup the original importing function
        old_importers = importing.importers # do once hopefully
    
    addonDir = os.path.dirname(os.path.abspath(__file__))
    libsDir = os.path.join(addonDir, "lib")
    if libsDir not in sys.path:
        sys.path.append(libsDir)
    
    from . import spreadsheet
    reload(spreadsheet)
    importer = ("Spreadsheet Import Plus (*.xlsx)", spreadsheet.SpreadsheetImporter)
    
    def importers(col):
        importers = list(old_importers(col))
        importers.append(importer)
        return tuple(importers)

    importing.importers = importers # patch the import function
