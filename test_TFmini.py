import serial
import statistics as st
import csv
ser = serial.Serial("/dev/ttyAMA0", 115200)
NormalVal = 69

def getTFminiData():
    #i = 0
    HeiList = []
    run = 0
    with open('145_6_19.csv', mode='w') as e:
                
        em_writer = csv.writer(e, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        em_writer.writerow(['col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7', 'col_8'])
        
        while True:
            count = ser.in_waiting
            if count > 8:
                recv = ser.read(9)
                ser.reset_input_buffer()
                if recv[0] == 89 and recv[1] == 89:
                    dis = recv[2] + recv[3] * 256
                    hei = NormalVal - dis
                    
                    if hei > 2: # 69 cm. is Narmal Distance Value between TFmini and floor  
                        HeiList.append(hei)
                        run = 0
                        #print ("if: %d " % hei)
                        #print("%s %s %s %s %s %s %s %s %s" %(str(recv[0]),str(recv[1]),str(recv[2]),str(recv[3]),str(recv[4]),str(recv[5]),str(recv[6]),str(recv[7]),str(recv[8])))
                   
                    else :
                        #HeiList.clear()
                        if run < 10 and hei != 0:
                            HeiList.append(hei)
                        else:
                            #print ("-----es: %d " % hei)
                            run = run+1
                            
                    if run > 1000 and len(HeiList) == 0:
                        print("Please check the box")
                        #HeiList.clear()
                        return None
                        
                    if run > 1000:
                        print("Successed!")
                        break
                        
                    #em_writer.writerow([recv[1],recv[2],recv[3],recv[4],recv[5],recv[6],recv[7],recv[8]])
                    
    return HeiList  

def getHei(arr):
    count = 0
    a = []
    tmp = 0
    hei = 0
    
    for k in range(0, len(arr)):
        i = int(arr[k])
        #print("last Tmp : %d"  %tmp)
        if i > tmp and count < 40 and i !=0:
            tmp = i
            count = 0
            
            #print (count)
        if i < tmp:
            break
        if i == tmp:
            print ("%d : %d " %(i,count))
            count += 1
            if count > 20:
                hei = tmp

        
        
    print ("temp : %d" % (hei))

if __name__ == '__main__':
    try:
        if ser.is_open == False:
            
            ser.open()
        print("Running")
        
        lines = getTFminiData()
        #print (len(a))
        #with open('dat.txt') as f:
        #    lines = f.readlines()
             
        b = []
        for i in lines:
            print (i)
            #a = i.split("\n")
            #k = int(a[0])
            #print(k)
            b.append(69 - i)
            #print(a)
        getHei(b)
        
    except KeyboardInterrupt:   # Ctrl+C
        if ser != None:
            ser.close()