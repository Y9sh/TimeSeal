from PySide6.QtCore import Qt, QTime
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (QPlainTextEdit)

class TextEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
    
    def check_text(self):
        if not self.toPlainText():
            self.insertPlainText(QTime.currentTime().toString("hh:mm") + ": ")
    
    def reflection_header(self,current_session_date):
        if not self.toPlainText():
            return self.appendPlainText(f"\n# -- Reflection: {current_session_date} --")
    
    def reflection_body(self,current_session_date):
        return (f"\n# -- Reflection: {current_session_date} --")
    
    def read_only(self,command):
        if command == 'YES':
            self.setReadOnly(True)
        else:
            self.setReadOnly(False)
        
    def keyPressEvent(self,event: QKeyEvent):
        # key_return refer to usual enter while key_enter for enter on numpad
        if event.key() == Qt.Key.Key_Return:
            self.insertPlainText("\n" + QTime.currentTime().toString("hh:mm") + ": ")
        else:
            super().keyPressEvent(event)