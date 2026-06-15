from PySide6.QtGui import QAction,QTextCursor,Qt,QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStatusBar,
    QFileDialog,
    QSplitter,
    QPushButton,
    QLabel,
    QWidget,
    QHBoxLayout
)

from core.editor import TextEditor
from core.file_man import FileManager
from core.debugging import print_line
from Ai_Engine.model import LocalModel
from Ai_Engine.metadata_engine import MetaData
from Ai_Engine.validation_manager import ValidManager
from Ai_Engine.LMstd_manager import LManager
import json
from pathlib import Path
import threading
import time
from queue import Queue

class MainWindow(QMainWindow):
    # main controller
    def __init__(self):
        super().__init__()
    
        self.setWindowTitle("Time Seal")
        self.resize(800,600)
        
        self.setStatusBar(QStatusBar(self))
        self.setup_services()
        self.default_state()
        self.file_manager.create_vaults()
        self.file_manager.check_git()
        self.load_today_session()
        self.setCentralWidget(self.editor)
        self.current_editor = self.editor
        self.toolbar()
        self.status_LM()
        self.status_load_model()
        self.refresh_server_status()
        
        
    # called mechanism
    def check_server_run(self):
       result = self.LM.LM_server('status')
       print_line(result)
       if 'The server is not running' in str(result):
           self.server_state = 'Offline'
       else:
           self.server_state = 'Online'
           
    def closeEvent(self,event):
        '''
        CLOSE APPS WILL STOP LM SERVER AND UNLOAD MODEL ONLY BEEN CALLED USING THE APP
        CLEAN-UP BEFORE CLOSE, SUCH AS, AUTO-SAVING BEFORE STOP APP
        MAYBE UNLOAD MODEL SHOULD USER DONE MANUALLY IF ITS MORE THAN 1
        '''
        event.accept()
        print_line(self.model.unload)
        self.save_file()
        if self.model.unload != '':
            self.model.unload_model()
        self.LM.LM_server('stop')
    
    def status_load_model(self):
        self.label_load = QLabel('Model:')
        self.loaded_model = QLabel("No Model")
        self.statusBar().addWidget(self.label_load)
        self.statusBar().addWidget(self.loaded_model)
        
        
    def status_LM(self):
        print_line(self.server_state)
        self.check_server_run()
        print_line(self.server_state)
        
        self.lm_stats = QLabel('LMstudio:')
        if self.server_state == 'Offline':
            self.server_button = QPushButton("🔴 Offline")
        else:
            self.server_button = QPushButton("🟢 Online")
            
        self.server_button.clicked.connect(self.toggle_server)
        
        self.statusBar().addWidget(self.lm_stats)
        self.statusBar().addWidget(self.server_button)
        self.statusBar().setStyleSheet("QStatusBar::item { border: none; }")
        
        #self.statusBar().addPermanentWidget(self.container)
    def updated_server_status(self):
        self.check_server_run()
        print_line(self.server_state)
        if self.server_state == 'Online':
            self.server_button.setText("🟢 Online")
        else:
            self.server_button.setText("🔴 Offline")
        
    def refresh_server_status(self):
        self.refresh_app_button = QPushButton("🗘")
        self.refresh_app_button.setFixedSize(30, 30)
        self.refresh_app_button.clicked.connect(self.updated_server_status)
        self.statusBar().addPermanentWidget(self.refresh_app_button)

        
    def toggle_server(self):
        if self.server_state == 'Offline':
            self.LM.LM_server('start')
            self.server_button.setText("🟢 Online")
            self.server_state = 'Online'
        else:
            self.LM.LM_server('stop')
            self.server_button.setText("🔴 Offline")
            self.server_state = 'Offline'
            
    def toolbar(self):
        
        open_file = QAction("Open",self)
        open_file.setStatusTip("Open File")
        open_file.triggered.connect(self.read_only_file)
        
        save_button = QAction("Save",self)
        save_button.setStatusTip("Save File")
        save_button.triggered.connect(self.save_file)
        
        reflection_button = QAction("Add Reflections", self)
        reflection_button.setStatusTip("Update old file")
        reflection_button.triggered.connect(self.add_reflections)
        
        today_button = QAction("Today Session",self)
        today_button.setStatusTip("Return to today session")
        today_button.triggered.connect(self.load_today_session)
        
        seal_button = QAction("Seal Time",self)
        seal_button.setStatusTip("Git commit notes")
        seal_button.triggered.connect(self.seal_time)
        
        menu = self.menuBar()
        
        file_menu = menu.addMenu("&File")
        file_menu.addAction(open_file)
        open_file.setShortcut('Ctrl+O')
        #file_menu.addSeparator()
        file_menu.addAction(save_button)
        save_button.setShortcut('Ctrl+S')
        file_menu.addAction(reflection_button)
        reflection_button.setShortcut('Ctrl+R')
        file_menu.addAction(today_button)
        today_button.setShortcut('Ctrl+T')
        file_menu.addAction(seal_button)
        seal_button.setShortcut('Ctrl+G')
        print("1ST:",self.mode)
        
        self.model_list = menu.addMenu("&Load Model")
        
        self.download_model_list_UI()
        refresh_button = QAction("Refresh",self)
        refresh_button.setStatusTip("Refresh models downloaded list")
        refresh_button.triggered.connect(self.thread_list_model)
        
        self.model_list.addAction(refresh_button)

    def thread_list_model(self):
        threading.Thread(target=self.refresh_model_list,daemon=True).start()
    
    def thread_model_switch(self,request_models):
        if self.switching:
            return
        threading.Thread(target=self.loads_model,args=(request_models,),daemon=True).start()
        
    def loads_model(self,request_model):
        list_load_model = self.model.list_model()
        parse_load = self.LM.model_parser(list_load_model,'models','loaded_instances')
        self.LM.append_list_model(parse_load)
        print_line(self.LM.loaded_model)
        self.model.load = request_model
        if request_model not in self.LM.loaded_model:
            print_line(self.model.load)
            print_line(self.model.unload)
            self.switching = True
            self.loaded_model.setText('Switching...')
            try:
                if self.model.unload != '':
                    self.model.unload_model()
                self.model.load_model()
            finally:
                self.switching = False
            print_line(self.model.unload)
        else:
            self.model.unload = request_model
            print_line(self.model.unload)
            print_line("Model already Load")
        self.loaded_model.setText(self.model.unload)
            
        
    def download_model_list_UI(self):
        try:
            cache_model = self.file_manager.read_json("Ai_Engine/cache_model.json",'r')
            if cache_model:
                for m in cache_model:
                    if m != None:
                        self.model_button = QAction(m,self)
                        self.model_button.triggered.connect(lambda checked = False, request_models=m:self.thread_model_switch(request_models))
                        self.model_list.addAction(self.model_button)
        except Exception as e:
            print(e)
            print("Server not run yet")
    
    def refresh_model_list(self):
        try:
            ask_server = self.model.list_model()
            parse_model = self.LM.model_parser(ask_server,'models','key')
            self.LM.append_list_model(parse_model)
            self.file_manager.write_json("Ai_Engine/cache_model.json",self.LM.list_model,'w')
            self.download_model_list_UI()
        except Exception as e:
            print(e)
        
    def setup_services(self):
        self.file_manager = FileManager()
        self.editor = TextEditor()
        self.model = LocalModel()
        self.metadata = MetaData()
        self.validation = ValidManager()
        self.LM = LManager()
        self.container = QWidget()
        self.layout_stat = QHBoxLayout(self.container)
        
    def default_state(self):
        self.mode = 'NORMAL'
        self.current_path = ""
        self.editor.read_only("NO")
        self.server_state = 'Offline'
        self.switching = False
        self.queues_path = Queue(maxsize=10)
        self.backprocess = threading.Thread(target=self.process_queue,daemon=True).start()
        
    def check_session(self):
        if self.file_manager.current_file_date in str(self.current_path):
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
        print_line(editrs)
        if editrs == 'MAIN':
            session = self.check_session()
            print_line(session)
            if session == 'TODAY_SESSION':
                editrs = self.editor
                text = editrs.toPlainText()
                print_line(editrs)
                print_line(act)
                self.file_manager.where_to_save(text,act,self.current_path)
            else:
                print("No save needed")
        else:
            print_line(self.mode)
            editrs = self.temp_editor
            print_line(editrs)
            print_line(act)
            content = editrs.toPlainText()
            body = content.replace(editrs.reflection_body(self.file_manager.current_file_date),"")
            if body:
                self.file_manager.where_to_save(text=body,action=act,current_pth=self.current_path)
                editrs.clear()
                editrs.close()
                self.restream_file()
            else:
                print("Nothing to save")
        
    def generate_metadata(self,path):
        date = self.file_manager.get_date(path).strftime("%Y-%m-%d")
        fragments = self.model.get_responses(path,model='')
        try:
            print_line(repr(fragments))
            cln =self.metadata.clean_response(fragments)
            print_line(repr(cln))
            json_obj = json.loads(cln)
        except json.JSONDecodeError as je:
            print_line("Invalid JSON",je)

        base_time_count = self.validation.time_count(path)
        if self.validation.check_time_exist(base_time_count) == False:
            print("No time in old notes")
            self.metadata.time = 'null'
        else:
            self.metadata.time = ''
        self.metadata.get_metadata(json_obj)
        
        after_gen_time = self.metadata.content_length
        validation = self.validation.check_times(base_time_count,after_gen_time)
        
        if validation == True or self.metadata.time == 'null':
            print("Metadata valid")
            self.metadata.build_metadata(date)
            print_line(self.metadata.metadatas)
            path = Path(f"{self.file_manager.metadata_dir}/{date}.json")
            self.file_manager.write_json(path,self.metadata.metadatas,'w')
            self.metadata.clean_block()
        else:
            self.metadata.clean_block()
            # later need to choose between regenerated using better model or cancel.
            print("Metadata need to regenerated")
            

    def read_only_file(self):
        self.close_and_clear_temp_editor()
        path,_= QFileDialog.getOpenFileName(self,"Open File",dir=str(self.file_manager.notes_vault))
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
                self.load_today_session()
        else: 
            print("User not choose any files")
            if self.mode != 'NORMAL':
                self.load_today_session()
            else:
                print("Current is NORMAL")
        metadata_valid = self.file_manager.check_metadata(self.current_path)
        if metadata_valid == True:
            print("Metadata exists")
        else:
            print_line(path)
            self.queues_path.put(path)
            print_line("Generate metadata")
    
    def process_queue(self):
        while True:
            try:
                print_line("Run")
                get_path = self.queues_path.get()
                print_line(get_path)
                self.generate_metadata(get_path)
            except Exception as err:
                print(err)
                print('continue')
                
    def load_today_session(self):
        self.mode = 'NORMAL'
        self.close_and_clear_temp_editor()
        print_line(self.current_path)
        if self.current_path == "":
            print_line(self.current_path)
            self.editor.check_text()
            self.current_path = self.file_manager.today_sessions
        
        today_file = self.file_manager.check_existed(self.file_manager.today_sessions)
        print_line(self.current_path,'what happens')
        print_line(today_file)
        if today_file == 'NO':
            print("NO")
            text = self.editor.toPlainText()
            self.file_manager.where_to_save(text,'a',self.current_path)
        else:
            self.current_path = str(self.file_manager.today_sessions)
            print_line(self.current_path)
            print("read")
            self.editor.read_only("NO")
            content = self.file_manager.read_file_silently(self.file_manager.today_sessions)
            self.editor.setPlainText(content)
            self.editor.moveCursor(QTextCursor.MoveOperation.End)


    def add_reflections(self):
        path = str(self.current_path)
        today_file_date =self.file_manager.current_file_date + ".md"
        
        print_line(path)
        print_line(today_file_date)
        print_line(self.mode)
        session = self.check_session()
        if session != 'TODAY_SESSION':
            self.mode = 'REFLECTIONS'
            self.current_path = path
            print_line(self.mode)
            print_line(self.current_path)
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
            print_line(self.mode)
          
    
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
    
    def seal_time(self):
        self.file_manager.commit()
    
        
app = QApplication([])
window = MainWindow()   
window.show()
app.exec()