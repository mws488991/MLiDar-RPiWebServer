import json, time
from loadcell import Loadcell
from flask import Flask, render_template, request
from tfmini import TFmini
from box import Box
from database_connect import Databaes_connect

import multiprocessing as mp

from RpiMotorLib import RpiMotorLib
    
GPIO_pins = (17, 27, 22)
direction= 20            
step = 21

motor = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")

app = Flask(__name__)
ld = Loadcell(5,6,214)
tf = TFmini()

bx = Box()
db = Databaes_connect()
#mt = Motor_step()


@app.route('/')
@app.route('/home')
def index():
    
    return render_template('index.html')    

#Connecting MLiDAR and return status
@app.route('/scanner')
def scanner_pg():  
      return render_template('scanner.html')    


@app.route('/scanner/scan', methods=['GET'])
def scaningfirst():
    #scan by TFMini
    p1 = mp.Process(target=stp_motor)
    p1.start()
    tf.calib()
    LiDlist = tf.getTFminiData()
    siz = tf.getSize(LiDlist)
    print(siz)
    bx.setLength(int(siz['wid']))  
    bx.setHeight(siz['hei']*10)
             
    return render_template('scanagian.html')

@app.route('/scanner/scanagin', methods=['GET'])
def scaning():
    #scan by TFMini
    if ld.setLoadcell():
        
        p1 = mp.Process(target=stp_motor)
        p1.start()
        
        
        
        LidList = tf.getTFminiData()
        siz = tf.getSize(LidList)
     
        if LidList == None:
            return '<h1 style="color:red;">กรุณาตรวจสอบอีกครั้งว่าคุณวางพัสดุแล้ว</h1>'
        time.sleep(10)
        print("Weigthing...")
        weight = ld.doWeight()
        
        if weight == 0:
            return '<h1 style="color:red;">พัสดุไม่ตรงตำแหน่ง</h1>'
        #print(weight)
        
        bx.setWidth(int(siz['wid']*10))
        bx.setWeight(int(weight))
        
        
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

def stp_motor():
    motor.motor_go(True, "Full" , 1200,.006, False, .05)

        
#webserver
if __name__=='__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')
    