import sys
import sqlite3
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from main_menu import MainMenu
import db_manager


db = sqlite3.connect("easypoint.db")
db_manager.create_initial_schema_if_needed()

app = QApplication(sys.argv)


menu = MainMenu()
menu.show()

app.exec()