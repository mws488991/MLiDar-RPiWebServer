import sys

class Loadcell():
    wei = 0
    def __init__(self, gpio1, gpio2, per_gram):
        self.gpio1 = gpio1
        self.gpio2 = gpio2
        self.EMULATE_HX711 = False
        self.referenceUnit = 1
        self.perGram = per_gram
        self.weight = 0

    def setLoadcell(self):
        
        if not self.EMULATE_HX711:
            import RPi.GPIO as GPIO
            from hx711 import HX711
        else:
            from emulated_hx711 import HX711

        def cleanAndExit():
            if not self.EMULATE_HX711:
                GPIO.cleanup()
                sys.exit()
        hx = HX711(self.gpio1,self.gpio2)
        hx.set_reading_format("MSB", "MSB")
        hx.set_reference_unit(self.referenceUnit)
        hx.reset()
        hx.tare()
        print ("LoadCell Setup")
        self.hx = hx
        return True
        
        
    def doWeight(self):
        last_wei = 0
        
        while True:
            
            try:
                val = self.hx.get_weight(5)
                if val < 1:
                    val = val * (-1)
                temp = int(val % 100)
                wei_gram = (val - temp) /  self.perGram
                if abs(last_wei - wei_gram) > 5:
                    self.weight = wei_gram
                    wei = wei_gram
                    print(wei_gram)
                elif abs(last_wei - wei_gram) < 30:
                    break
                    
                last_wei = int(wei_gram)
                self.hx.power_down()
                self.hx.power_up()
                
                
            except (KeyboardInterrupt, SystemExit):
                cleanAndExit()
                return 0
        we = self.weight
        
        #print(we)
        return we
'''
a = Loadcell(5,6,214)
a.setLoadcell()
input("Enter")
b = a.doWeight()
print (b)'''