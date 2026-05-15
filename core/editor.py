from PySide6.QtCore import Qt, QTime
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (QPlainTextEdit)

class TextEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.check_text()
    
    def check_text(self):
        if not self.toPlainText():
            self.insertPlainText(QTime.currentTime().toString("hh:mm") + ": ")
        
            
    def keyPressEvent(self,event: QKeyEvent):
        # key_return refer to usual enter while key_enter for enter on numpad
        if event.key() == Qt.Key.Key_Return:
            self.insertPlainText("\n" + QTime.currentTime().toString("hh:mm") + ": ")
        else:
            super().keyPressEvent(event)