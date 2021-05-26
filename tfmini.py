import sys, serial, time, array
import numpy as np
import statistics as st
class TFmini():
   
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyAMA0", 115200) 
        
        #self.unit_cm = 24.57284 # number unit per one centimater
        self.lidar_per_sec = 127.64107
        self.rate_speed = 4.906
        self.calib_no = 70;

    def calib(self):
        print(self.ser.is_open)
        if self.ser.is_open == False:
                self.ser.open()
        cal = []
        i = 0
        while True:
            
            count = self.ser.in_waiting
            
            if count > 8:
                recv = self.ser.read(9)  #Read array from LiDar
                self.ser.reset_input_buffer()
                if recv[0] == 89 and recv[1] == 89: # 0x59 is 'Y'
                    distance = recv[2] + recv[3] * 256
                    #print(distance)
                    cal.append(distance)
                    #print(distance)
                    if len(cal) == 120:
                        #print("Cal Successed")
                        self.calib_no = st.mode(cal)
                        print("Calibrate Finished" + str(self.calib_no))
                        return self.calib_no
            i=i+1; 
            
    def getTFminiData(self):
        if self.ser.is_open == False:
                self.ser.open()
        
        disList = []
         
        i = 0
        run = 0
        #print("Scanning!")
        
        try:
            while True:
                count = self.ser.in_waiting
                if count > 8:
                   
                    recv = self.ser.read(9)  #Read array from LiDar
                    self.ser.reset_input_buffer()
                    #print(recv)
                    if recv[0] == 89 and recv[1] == 89: # 0x59 is 'Y'
                        #print(i)
                        #recv 2 is distance 
                        distance = recv[2] + recv[3] * 256                
                        height = abs(distance - self.calib_no)
                        #print(distance)
                        
                        if height > 2:
                            disList.append(height)
                            run = 0
                        
                        #ป้องกันการแกว่งโดยไม่หยุดในทันที
                        if len(disList) > 1 and height < 2:
                            run = run+1;
                            
                        #ป้องกันการแกว่งของข้อมูล
                        if run > 500:
                            #print("RUN > 120")
                            print("Get Successed")
                            break;
                else:
                    
                    pass

            print("TFMini Finished")
            
            return disList
        except AssertionError as e:
            print(e)
            return None

    def getSize(self,disList):
        ss = self.rate_speed * (len(disList)/self.lidar_per_sec)
         
        obj = {
            'hei': np.max(disList),
            'wid':  ss,
         }
        return obj