import json, time
from loadcell import Loadcell
from flask import Flask, render_template, request
from tfmini import TFmini
from box import Box
from database_connect import Databaes_connect
    
app = Flask(__name__)
ld = Loadcell(5,6,214)
tf = TFmini()
crlib = tf.calib()
bx = None
db = Databaes_connect()



@app.route('/')
@app.route('/home')
def index():
    
    return render_template('index.html')    

#Connecting MLiDAR and return status
@app.route('/scanner')
def scanner_pg():  
      
      return render_template('scanner.html')    



@app.route('/scanner/scan', methods=['GET'])
def scaning():
    #scan by TFMini
    if ld.setLoadcell():
        print("Add Item")
        time.sleep(2)
        obj = tf.getTFminiData(crlib)
        if obj == None:
            return '<h1 style="color:red;">Time Over</h1>'
        print(obj)
        
        time.sleep(2)
        ld.doWeight() 
        weight = ld.getWeight()
        
        global bx
        bx = Box(int(weight),int(obj['wid']*10),int(obj['hei']*10))
        
    else :
        print("Calibrate Error")
    
    box = bx.getBox()
    item = {
        'frm_display': "block",
        'tnf_display': "none",
        'clr_btn' : "block",
        'sc_btn' : "none",
        'wei': box['weight'],
        'wid' : box['width'],
        'len' : box['length'],
        'hei' : box['height'],
        }
    
    return render_template('infomation.html', **item)  

@app.route('/scanner/scan', methods=['POST','GET'])
def objItem():
    
    #print("Post")
    if request.method == 'POST':
       sender = request.form['sender']
       addressee = request.form['addressee']
       
    else:
       sender = request.args.get('sender')
       addressee = request.args.get('addressee')
       
    bx.setAddress(sender,addressee)
    box = bx.getBox()
    bx.genTrackNo()
    bx.addBox()
    
    
    item = {
        'frm_display': "none",
        'tnf_display': "block",
        'clr_btn' : "block",
        'sc_btn' : "none",
        'des_display': "none",
        'track_no': bx.getTrack(),
        'description_form': box['sender'],
        'description_send': box['addressee'],
    }
    
    return render_template('infomation.html', **item)
    
@app.route('/track')
def track():
    tem = {
        'frm_display' : "block",
        }
    return render_template('track.html',**tem)

@app.route('/track/find',methods=['POST','GET'])
def findTrack():
    date = ""
    sender = ""
    addressee = ""
    cl = "red"
    #Search data in DB table
    
    if request.method == 'POST':
       trackNo = request.form['trackNo']
    else:
       trackNo = request.args.get('trackNo')
    
    conn = db.create_connection()
    
    st = db.search_trackNo(conn,trackNo)
    
    if st == None:
        trackNo = "'" + trackNo +"'" + " No this Track!"
    else :
        date = "Date: " + st[0]
        sender = "Sender: " + st[6]
        addressee = "Addressee: " + st[7]
        cl = "#228b22"
        
    
    
    boxObj = {
        'cl': cl,
        'trackNo': trackNo,
        'date': date,
        'sender': sender,
        'addressee' : addressee,
    }
    return render_template('track.html',**boxObj)

@app.route('/document')
def document():
    conn = db.create_connection()
    rows = db.list_table(conn)
    return render_template('document.html',rows=rows)

@app.route('/del/<track>',methods=['POST', 'GET'])
def delete(track):
    conn = db.create_connection()
    db.delete_data(conn,track)
    return document()

@app.route('/edit/<trackNo>',methods = ['POST','GET'])
def edit_pg(trackNo):
    conn = db.create_connection()
    rows = db.search_trackNo(conn,trackNo)
    
    print (rows[1])
    return render_template('editadd.html',rows=rows)

@app.route('/editt/<trackNo>',methods=['POST', 'GET'])
def editAdd(trackNo):
    if request.method == 'POST':
       sender = request.form['sender']
       address = request.form['address']
    else:
       sender = request.args.get('sender')
       address = request.args.get('address')
       
    conn = db.create_connection()
    db.edit_data(conn,trackNo,sender,address)
    
    return document()



if __name__=='__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
    