from PySide6.QtCore import QDate
from PySide6.QtGui import QAction,QTextCursor
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStatusBar,
    QFileDialog,
)
from editor import TextEditor
from file_man import FileManager
             
class MainWindow(QMainWindow):
    # main controller
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Time Notes")
        self.resize(600,500)
        
        self.file_manager = FileManager()
        self.editor = TextEditor()
        
        self.load_current_file()
        self.setCentralWidget(self.editor)
        button_action = QAction("Open",self)
        button_action.setStatusTip("Open File")
        button_action.triggered.connect(self.read_only_file)
        
        button_act_1 = QAction("Save",self)
        button_act_1.setStatusTip("Save File")
        self.setStatusBar(QStatusBar(self))
        button_act_1.triggered.connect(self.save_file)
        
        button_act_2 = QAction("Add Reflections", self)
        button_act_2.setStatusTip("Update old file")
        self.setStatusBar(QStatusBar(self))
        button_act_2.triggered.connect(self.add_reflections)
        
        menu = self.menuBar()
        
        file_menu = menu.addMenu("&File")
        file_menu.addAction(button_action)
        #file_menu.addSeparator()
        file_menu.addAction(button_act_1)
        file_menu.addAction(button_act_2)
        
    
    # called mechanism
    def save_file(self):
        text = self.editor.toPlainText()
        self.file_manager.check_for_existed_file(text)
        
    def read_only_file(self):
        path,_= QFileDialog.getOpenFileName(self,"Open File",dir='./notes')
        current_file = self.file_manager.current_file_date
        
        print("Read only current",current_file)
        print("Read only path:",path)
        if current_file not in path:
            print("Enter read only")
            content= self.file_manager.read_file(path)
            self.file_manager.current_path = path
            print("Current path:",self.file_manager.current_path)
            self.editor.setReadOnly(True)
            self.editor.setPlainText(content)
            self.editor.moveCursor(QTextCursor.MoveOperation.End)
        else:
            content = self.file_manager.read_file(path)
            self.file_manager.current_path = f"./notes/{current_file}.md"
            self.editor.setReadOnly(False)
            self.editor.setPlainText(content)
            self.editor.moveCursor(QTextCursor.MoveOperation.End)
    
    def load_current_file(self):
        try:
            content = self.file_manager.read_file_silently()
            self.editor.setPlainText(content)
            self.editor.moveCursor(QTextCursor.MoveOperation.End)
        except FileNotFoundError:
            print("Not found any file...next save will create current date note") 
            
    def add_reflections(self):
        path = str(self.file_manager.current_path)
        current_file =self.file_manager.current_file_date
        print("Path",path)
        print("Current:",current_file)
        if path not in current_file:
            self.editor.appendPlainText(f"#-- Refer to Old Timeline: {self.file_manager.get_date(path)}")
            self.editor.appendPlainText(f"#-- Reflection: {self.file_manager.current_file_date} --")
            self.editor.moveCursor(QTextCursor.MoveOperation.End)
            print("tRIGGERED TEMPORARY EDITOR")
        
app = QApplication([])
window = MainWindow()
window.show()
app.exec()