from database_connect import Databaes_connect
import datetime 

class Box:
    
    def __init__(self):
        self.box = {
            'dateOder': datetime.datetime.now(),
            'weight': 0,
            'width' : 0,
            'length' : 0,
            'height' : 0,
            'trackNo': '',
            'sender': "",
            'addressee': "",
            }
        
    def getTrack(self):
        return  self.box['trackNo']
    
    def getWeigth(self):
        return  self.box['weight']
    
    def setAddress(self,sender,addressee):
        self.box['sender'] = str(sender)
        self.box['addressee'] = str(addressee)
        
    def setWeight(self,wei): 
        self.box['weight'] = wei
        
    def setHeight(self,hei):
        self.box['height'] = hei
        
    def setLength(self,leng):
        self.box['length'] = leng
    
    def setWidth(self,wid):
        self.box['width'] = wid
    
    
    #generate this Track No.
    def genTrackNo(self):
        db = Databaes_connect()
        conn = db.create_connection()
        while True:
            x = datetime.datetime.now()
            st = "MLD" + str(x.day) + str(x.year) + str(x.hour + x.minute + x.microsecond)
            if (db.search_trackNo(conn,st))== None:
                self.box['trackNo'] = st
                return st
            else:
                print ("Cann't")
                
    def getBox(self):
        return self.box
    
    def addBox(self):
        task = (self.box['dateOder'],self.box['trackNo'] ,int(self.box['weight']),int(self.box['width']) ,int(self.box['height']) ,int(self.box['length']),self.box['sender'] , self.box['addressee'])
        db = Databaes_connect()
        conn = db.create_connection()
        with conn:
            db.insert_data(conn, task)
        
