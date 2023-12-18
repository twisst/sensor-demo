import machine
from machine import Pin
import time

led = Pin(15, Pin.OUT)
button = Pin(17, Pin.IN, Pin.PULL_UP)
photo_pin = machine.ADC(26)

checkSensor = False
led.off()

while True:
    
    if button.value() == False:
        led.toggle()
        time.sleep(0.3)
        checkSensor = not checkSensor
        print("LDR", checkSensor)
        
    if checkSensor:
        val = photo_pin.read_u16()
        print(val)
        time.sleep_ms(52)

