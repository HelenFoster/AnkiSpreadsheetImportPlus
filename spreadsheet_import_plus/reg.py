# Copyright (C) 2020  Helen Foster
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import os
import sys
from importlib import reload

from aqt.utils import showText
import anki.importing as importing

def register(again=False):
    """Register the new importer with Anki's importers."""
    
    addonDir = os.path.dirname(os.path.abspath(__file__))
    libsDir = os.path.join(addonDir, "lib")
    if libsDir not in sys.path:
        sys.path.append(libsDir)
    
    from . import spreadsheet
    reload(spreadsheet)
    importer = (("Spreadsheet Import Plus (*.xlsx)", spreadsheet.SpreadsheetImporter),)
    if again:
        importing.Importers = importing.Importers[0:-1] + importer
        showText(repr(importing.Importers))
    else:
        importing.Importers += importer
