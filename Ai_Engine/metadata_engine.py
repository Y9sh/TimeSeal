# here will parsing the each metadata for visual usage or even RAG later.
# here were metadata will be builds

class MetaData:
    def __init__(self):
        self.block = []
        self.time = ''
            
    def get_metadata(self,contents):
        for items in contents:
            print("what",self.time)
            if self.time == 'null':
                self.block.append({
                    "time":self.time,
                    "summary":items['summary'],
                    "tags":items['tags']
                })
            else:
                self.block.append({
                    "time":items['times'],
                    "summary":items['summary'],
                    "tags":items['tags']
                })
        self.content_length= len(contents)
    
    def build_metadata(self,date):
        self.metadatas = {
            "date":date,
            "entry_count":self.content_length,
            "blocks": self.block
        }
    
    def clean_block(self):
        self.block = []
        
    def clean_response(self,content):
        c =content.replace("'","")
        cc = c.replace('`',"")
        return cc.replace('json',"")