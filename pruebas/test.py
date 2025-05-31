import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout
from PySide6.QtGui import Qt

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Margins")
        self.setFixedSize(350, 220)
        fixedWidth = 150

        usernameText = QLabel("Username: ")
        usernameLine = QLineEdit("")
        usernameLine.setFixedWidth(fixedWidth)

        pinText = QLabel("PIN: ")
        pinLine = QLineEdit("")
        pinLine.setFixedWidth(fixedWidth)

        pinConfirmText = QLabel("Confirm PIN: ")
        pinConfirmLine = QLineEdit("")
        pinConfirmLine.setFixedWidth(fixedWidth)

        userLayout = QHBoxLayout()
        userLayout.addWidget(usernameText)
        userLayout.addWidget(usernameLine)

        pinLayout = QHBoxLayout()
        pinLayout.addWidget(pinText)
        pinLayout.addWidget(pinLine)

        confirmLayout = QHBoxLayout()
        confirmLayout.addWidget(pinConfirmText)
        confirmLayout.addWidget(pinConfirmLine)

        v_layout = QVBoxLayout()
        v_layout.addLayout(userLayout)
        v_layout.addLayout(pinLayout)
        v_layout.addLayout(confirmLayout)
        v_layout.setSpacing(50)
        #v_layout.setContentsMargins(1,1,1,1)
        v_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(v_layout)

app = QApplication(sys.argv)

wid = Widget()
wid.show()

app.exec()

        
