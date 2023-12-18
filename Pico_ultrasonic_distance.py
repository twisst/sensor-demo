import machine
from machine import Pin
from time import sleep
from picozero import DistanceSensor

# print unieke id van deze Pico
s = machine.unique_id()
for b in s:
    print(hex(b)[2:], end="")
print(" ultrasonic")

led = Pin(10, Pin.OUT)
button = Pin(20, Pin.IN, Pin.PULL_UP)

# mijn ultrasone afstandssensor is geen 'P' of '+' en is dus bedoeld voor 5V.
# om dat te fiksen zit er een voltage divider in: 1K tussen echo en pin 2 en 2K van pin 2 naar GND
ds = DistanceSensor(echo=2, trigger=3, max_distance=1.5)

checkSensor = False
led.off()

while True:
    
    if button.value() == False:
        led.toggle()
        sleep(0.3)
        checkSensor = not checkSensor
        print("ultrasonic", checkSensor)
        
    if checkSensor:
        d = ds.distance
        if d < 1.5:
            print(round(d * 1000)) # multiply by 1000 to get millimeters
        sleep(0.07)

