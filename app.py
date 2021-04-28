import json
import time
from flask import Flask, render_template, request
app = Flask(__name__)
global ObjItem 

ObjItem = {
        'weight': 0,
        'width' : 0,
        'lenght': 0,
        'heigth': 0,
        'trackNo' : "",
        'faar': "",
        'sddr': "",
    }

@app.route('/')
@app.route('/home')
def index():
    #แสดงว่าเครื่องพร้อมมาก สำหรับการใช้งาน คืนค่าแสดงผลว่าเครื่องทำงานแล้ว 
    #เช็คว่าเครื่องชั่ง/Lidar พร้อมทำงานหรือไม่ และแสดงผลที่หน้าจอ
    return render_template('index.html')    


#Connecting MLiDAR and return status
@app.route('/scanner')
def scannerStatus():  

    #เช็คว่าเครื่องทำงานหรือไม่ หากไม่ให้แสดงผลว่าอะไรกำลังบกพร่อง 
    #เครื่องพร้อมใช้งาน Calibate เครื่องชั่งให้เรียบร้อย
    # x = int(random.random()*1000)%2
    time.sleep(1)
    x=1
    if x == 1:
        tus = {
            'col':"green",
            'mlidar_Status' : "พร้อมใช้งาน!",
            'description_title': "กรุณาวางพัสดุบนตำแหน่งชั่ง",
            'description_detail': "จากนั้นคลิ๊กปุ่ม Scan",
            'dis': "none",
        }
    else : 
        tus = {
            'col':"red",
            'mlidar_Status' : "No Ready!",
            'description_title': "โปรดตรวจเช็คให้แน่ใจว่าคุณได้เปิดเครื่องเมลิดาร์แล้ว",
            'description_detail': "จากนั้นให้กด RESET รอเครื่องทำงาน",
            'dis': "none",
        }
    return render_template('scanner.html',**tus)    

@app.route('/scanner/scan')
def scaning():
    #รับน้ำหนังจาก Loadcell
    #รอการคืนค่าของขนาด จาก Lidar
    time.sleep(1)
    x = int(random.random()*1000)%2

    item = {
        'weight': 578.9,
        'width' : 22,
        'lenght': 15,
        'heigth': 10,
        'trackNo' : "MLD0000000"
    }
    
    if x ==1:
            
        boxObj = {
            'col':"yellow",
            'mlidar_Status' : "เสร็จสิ้น!",
            'description_title': item,
            'description_detail': "",
            'dis': "block",
            
        }
    else:
        boxObj = {
            'col':"red",
            'mlidar_Status' : "ผิดพลาด !",
            'description_title': "ตรวจสอบให้แน่ใจว่าคุณวางพัสดุในตำแหน่งที่ถูกต้อง",
            'description_detail': "จากนั้นคลิ๊กปุ่ม Scan",
            'dis': "none",
        }
    return render_template('scanner.html', **boxObj)  

@app.route('/scanner/scan' , methods=['POST','GET'])
def objItem():
    
    if request.method == 'POST':
      faddr = request.form['faddr']
      saddr = request.form['saddr']    
    else:
      faddr = request.args.get('faddr')
      saddr = request.args.get('saddr')

    boxObj = {
        'dis': "none",
        'genTrack': "TRACK",
        'description_detail':'NUMBER',
        'description_form': 'Form: ' + faddr,
        'description_send': 'Send: ' + saddr,
    }
    return render_template('scanner.html', **boxObj)


@app.route('/add')
def addItem():
    boxObj = {
        'engSta' : "!",
        'genTrack': "MLD0000000",
        'description_detail': "578.9g, 22, 15, 10",
        
    }
    return render_template('document.html', **boxObj)

@app.route('/track')
def track():
    boxObj = {
        'genTrack': " ",
        'description_detail': " ",
    }
    return render_template('track.html',**boxObj)

@app.route('/track/find',methods=['POST'])
def findTrack():
    #Search data in DB table 
    x = dict(request.form.items())
   
    boxObj = {
        'genTrack': x["trackNo"],
        'description_detail': trackNo,
    }
    return render_template('track.html',**boxObj)    



if __name__=='__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
    