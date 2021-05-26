import multiprocessing as mp
from tfmini import TFmini
from RpiMotorLib import RpiMotorLib
import time
from loadcell import Loadcell
import csv

GPIO_pins = (17, 27, 22)
direction= 20            
step = 21

motor = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")
a = TFmini()
ld = Loadcell(5,6,214)

       

def run():
    ld.setLoadcell()
    
    p1 = mp.Process(target=stp_motor)
    p1.start()
       
    disList1 = a.getTFminiData()
    
        
    print("Please Return ")
    input("Enter if you returned")
    
    p1 = mp.Process(target=stp_motor)
    p1.start()
    
    disList2 = a.getTFminiData()
    r1 = a.getWid(disList1)
    r2 = a.getWid(disList2)
    time.sleep(12)
    weigth = ld.doWeight()
    print(weigth)
    
    
    print("Height: " +  str(r1['hei']))
    print("Height: " +  str(r2['hei']))
    print("Width: " +  str(r1['wid']))
    print("Lenght: " +  str(r2['wid']))
    print("Weight: " + str(weigth))
    with open('145_6_19.csv', mode='a') as e:
        em_writer = csv.writer(e, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #em_writer.writerow(['Height_1', 'Height_2', 'Widght', 'Lenght', 'Weight'])
        em_writer.writerow([r1['hei'],r2['hei'],r1['wid'],r2['wid'],weigth])
    
def stp_motor():
    motor.motor_go(True, "Full" , 1500,.006, False, .05)


if __name__=="__main__":
    for i in range(10):
        input("Raddy ?")
        run()
        