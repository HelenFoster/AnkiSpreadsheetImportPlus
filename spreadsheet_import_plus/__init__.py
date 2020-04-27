# Copyright (C) 2020  Helen Foster
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from importlib import reload

from aqt import mw
from aqt.qt import QAction

from . import reg

def reregister():
    reload(reg)
    reg.register(again=True)

config = mw.addonManager.getConfig(__name__)
if config["debug"]:
    action = QAction("Reload SpreadsheetImportPlus", mw)
    action.triggered.connect(reregister)
    mw.form.menuTools.addAction(action)

reg.register(again=False)
