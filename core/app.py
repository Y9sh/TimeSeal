from PySide6.QtGui import QAction,QTextCursor,Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStatusBar,
    QFileDialog,
    QSplitter
)

#from core.editor import TextEditor
#from core.file_man import FileManager
from editor import TextEditor
from file_man import FileManager
       
class MainWindow(QMainWindow):
    # main controller
    def __init__(self):
        super().__init__()
    
        self.setWindowTitle("Time Seal")
        self.resize(800,600)
        self.file_manager = FileManager()
        self.editor = TextEditor()
        
        self.file_manager.check_dir_notes()
        self.default_state()
        self.load_today_session()
        self.setCentralWidget(self.editor)
        self.current_editor = self.editor
        
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
        
        button_act_3 = QAction("Today Session",self)
        button_act_3.setStatusTip("Return to today session")
        self.setStatusBar(QStatusBar(self))
        button_act_3.triggered.connect(self.load_today_session)
        
        menu = self.menuBar()
        
        file_menu = menu.addMenu("&File")
        file_menu.addAction(button_action)
        #file_menu.addSeparator()
        file_menu.addAction(button_act_1)
        file_menu.addAction(button_act_2)
        file_menu.addAction(button_act_3)
        
        print("1ST:",self.mode)
    
    # called mechanism
    def default_state(self):
        self.mode = 'NORMAL'
        self.current_path = ""
        self.editor.read_only("NO")
    
    def check_session(self):
        if self.file_manager.current_file_date in self.current_path:
            if self.mode == 'NORMAL':
                return 'TODAY_SESSION'
        else:
            return 'OLD_SESSION'
        
    def actions_decisions(self,curr_mode):
        
        if curr_mode == 'NORMAL':
            curr_editor = 'MAIN'
            action = 'w'
            return curr_editor,action
        else: 
            curr_editor = 'TEMP'
            action = 'a'
            return curr_editor ,action
    
    def save_file(self):
        editrs, act = self.actions_decisions(self.mode)
        print("Editor:",editrs)
        if editrs == 'MAIN':
            session = self.check_session()
            print("SAVE SESSION:",session )
            if session == 'TODAY_SESSION':
                editrs = self.editor
                text = editrs.toPlainText()
                print("HERE SAVING HAPPENS:",editrs,act)
                self.file_manager.where_to_save(text,act,self.current_path)
            else:
                print("No save needed")
        else:
            print("MOde in saveing ",self.mode)
            editrs = self.temp_editor
            print("HERE REFLECTION SAVING HAPPENS:",editrs,act)
            content = editrs.toPlainText()
            body = content.replace(editrs.reflection_body(self.file_manager.current_file_date),"")
            if body:
                self.file_manager.where_to_save(text=body,action=act,current_pth=self.current_path)
                editrs.clear()
                editrs.close()
                self.restream_file()
            else:
                print("Nothing to save")
                
    def read_only_file(self):
    
        self.close_and_clear_temp_editor()
        path,_= QFileDialog.getOpenFileName(self,"Open File",dir='./notes')
        if path:
            today_session = self.file_manager.today_sessions
            
            choosen_file = self.file_manager.save_decisions(path,today_session)
            self.current_path = path
            content = self.file_manager.read_file(choosen_file)
            self.editor.setPlainText(content)
            
            session = self.check_session()
            if session == 'OLD_SESSION':
                self.editor.read_only("YES")
            else:
                '''
                self.mode = 'NORMAL'
                self.editor.read_only("NO")
                self.editor.moveCursor(QTextCursor.MoveOperation.End)
                '''
                self.load_today_session()
        else: 
            print("User not choose any files")
            if self.mode != 'NORMAL':
                self.load_today_session()
            else:
                print("Current is NORMAL")

    def load_today_session(self):
        self.mode = 'NORMAL'
        self.close_and_clear_temp_editor()
        if self.current_path == "":
            self.editor.check_text()
            self.current_path = str(self.file_manager.today_sessions)
        
        today_file = self.file_manager.check_existed(self.file_manager.today_sessions)
        if today_file == 'NO':
            text = self.editor.toPlainText()
            self.file_manager.where_to_save(text,'a',self.current_path)
        else:
            self.current_path = str(self.file_manager.today_sessions)
            print("read")
            self.editor.read_only("NO")
            content = self.file_manager.read_file_silently(self.file_manager.today_sessions)
            self.editor.setPlainText(content)
            self.editor.moveCursor(QTextCursor.MoveOperation.End)


    def add_reflections(self):
        path = str(self.current_path)
        today_file_date =self.file_manager.current_file_date + ".md"
        
        print("Last Path",path)
        print("Current:",today_file_date)
        print("MODES:",self.mode)
        session = self.check_session()
        if session != 'TODAY_SESSION':
            self.mode = 'REFLECTIONS'
            self.current_path = path
            print("REFLC:",self.mode)
            print("Should be the latest path",self.current_path)
            splitter = QSplitter(Qt.Vertical)
            self.temp_editor = TextEditor()
            
            self.current_editor = self.temp_editor
            self.temp_editor.reflection_header(self.file_manager.current_file_date)
            splitter.addWidget(self.editor)
            splitter.addWidget(self.temp_editor)
            
            
            self.temp_editor.moveCursor(QTextCursor.MoveOperation.End)
            print("tRIGGERED TEMPORARY EDITOR")
            self.setCentralWidget(splitter)
        else:
            self.close_and_clear_temp_editor()
            self.mode = 'NORMAL'
            print("Hehe not today",self.mode)
          
    
    def restream_file(self):
        self.mode = 'ARCHIVE'
        content = self.file_manager.read_file_silently(self.current_path)
        self.editor.setPlainText(content)
    
    def close_and_clear_temp_editor(self):
        try:
            self.temp_editor.clear
            self.temp_editor.close()
        except AttributeError:
            print("No temp editor yet")
            

app = QApplication([])
window = MainWindow()   
window.show()
app.exec()