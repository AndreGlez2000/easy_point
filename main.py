import sys
import sqlite3
from PySide6.QtWidgets import QApplication
from main_menu import MainMenu

db = sqlite3.connect("easypoint.db")

app = QApplication(sys.argv)

menu = MainMenu()
menu.show()

app.exec()