import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import multiprocessing as mp


#define GPIO pins
GPIO_pins = (17, 27, 22)
direction= 20            
step = 21                


motor = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")
    
#class Motor_step():
    
def motor_step_run():
    #print ("Motor Running")
    motor.motor_go(False, "Full" , 1500,.006, False, .05) 
    #motor.motor_stop()
    
    
def motor_step_stop():
    self.st = False


if(__name__=='__main__'):
    p1 = mp.Process(target=motor_step_run)
    p1.start()
    print('สั่งงานไปแล้ว')
    name = input("Enter name: ")
    print (name)