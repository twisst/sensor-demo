import board
import time
import digitalio
import keypad
import asyncio
import supervisor

import busio
import adafruit_tcs34725

i2c = busio.I2C(board.GP21, board.GP20)

LED = digitalio.DigitalInOut(board.GP18)
LED.direction = digitalio.Direction.OUTPUT
LED.value = False

brightLED = digitalio.DigitalInOut(board.GP15)
brightLED.direction = digitalio.Direction.OUTPUT
brightLED.value = False

# object om te onthouden wat we aan het doen zijn
class Controls:
    def __init__(self):
        self.sensorRunning = False
        self.sensor = adafruit_tcs34725.TCS34725(i2c)
        self.inputVal = 0


async def monitor_buttons(knop_kleurensensor_pin, controls):
    # Monitor buttons for input/output selection.
    
    keys = keypad.Keys((knop_kleurensensor_pin,), value_when_pressed=False, pull=True)

    while True:
        key_event = keys.events.get()
        
        if key_event and key_event.pressed:
            key_number = key_event.key_number
            
            if key_number == 0: # the first sensor is the toggle to the colour sensor
                controls.sensorRunning = not controls.sensorRunning
        
        # allow other tasks to do work
        await asyncio.sleep(0)
            

async def toggleSensing(controls):
    # turn LEDs on or off, stop or start sensing
    
    global LED, brightLED
    toggle = False
    
    while True: # start over
        
        while toggle == controls.sensorRunning: # do nothing until things change
            # allow other tasks to do work
            await asyncio.sleep(0)
            continue
        toggle = controls.sensorRunning
        
        LED.value = controls.sensorRunning
        brightLED.value = controls.sensorRunning
        
        print("Colour", controls.sensorRunning)
        
        # if we just told the sensor to start sensing, then let's do so
        if controls.sensorRunning:
            sensor_task = asyncio.create_task(printSensorValues(controls))
            await asyncio.gather(sensor_task) # wait until the sensor stops
        
        # allow other tasks to do work
        await asyncio.sleep(0)



async def printSensorValues(controls):
    
    sensor = controls.sensor
    
    while controls.sensorRunning:
        
        print('Colour: ({0}, {1}, {2})'.format(*sensor.color_rgb_bytes), end="; ")
        print('temp: {0}K'.format(sensor.color_temperature), end="; ")
        print('Lux: {0}'.format(sensor.lux))

        await asyncio.sleep(0)
        await asyncio.sleep(0.7)


async def readSerial(controls):
    
    from usbreader import usb_reader # from usbreader.py
    
    while True:
        controls.inputVal = usb_reader.read()  # read until newline, echo back chars
        #mystr = usb_reader.read(end_char='\t', echo=False) # trigger on tab, no echo
#         if controls.inputVal:
#             print("input:", controls.inputVal, end='')
        await asyncio.sleep(0)

       
async def main():
    
    controls = Controls()
    
    # first, identify as the Pico with the colour sensor
    print("Colour", controls.sensorRunning)
    
    # stand-by to turn the LEDs on or off and stop or start the sensing
    sensor_toggle = asyncio.create_task(
        toggleSensing(controls)
    )
    
    # start keeping an eye on the button
    buttons_task = asyncio.create_task(
        monitor_buttons(board.GP17, controls)
    )
    
    # read values coming in
    serialInput = asyncio.create_task(
        readSerial(controls)
    )
    
    # This will run forever:
    await asyncio.gather(sensor_toggle, buttons_task, serialInput)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('keyboard interrupt')
finally:
    print('Program finished')
    LED.value = False
    brightLED.value = False





    
    

'''
    color_rgb_bytes - A 3-tuple of the red, green, blue color values.  These are returned as bytes from 0 to 255 (0 is low intensity, 255 is maximum intensity).
    color_temperature - The color temperature in Kelvin detected by the sensor.  This is computed from the color and might not be super accurate!
    lux - The light intensity in lux detected by the sensor.  This is computed from the color and might not be super accurate!
'''

# more about calibration here:
# https://github.com/systembolaget/Physical-computing-sensor-servo-tutorial-6a-Colour-finder-with-ams-TCS34725-and-HD-1900A
# https://learn.adafruit.com/adafruit-color-sensors/library-reference#interrupts-and-led-control


'''
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the TCS34725 color sensor.
# Will detect the color from the sensor and print it out every second.
import time
import board
import adafruit_tcs34725


# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_tcs34725.TCS34725(i2c)

# Change sensor integration time to values between 2.4 and 614.4 milliseconds
# sensor.integration_time = 150

# Change sensor gain to 1, 4, 16, or 60
# sensor.gain = 4

In addition there are some properties you can both read and write to change how the sensor behaves:

    integration_time - The integration time of the sensor in milliseconds.  Must be a value between 2.4 and 614.4.
    gain - The gain of the sensor, must be a value of 1, 4, 16, 60.



# Main loop reading color and printing it every second.
while True:
    # Raw data from the sensor in a 4-tuple of red, green, blue, clear light component values
    # print(sensor.color_raw)

    color = sensor.color
    color_rgb = sensor.color_rgb_bytes
    print(
        "RGB color as 8 bits per channel int: #{0:02X} or as 3-tuple: {1}".format(
            color, color_rgb
        )
    )

    # Read the color temperature and lux of the sensor too.
    temp = sensor.color_temperature
    lux = sensor.lux
    print("Temperature: {0}K Lux: {1}\n".format(temp, lux))
    # Delay for a second and repeat.
    time.sleep(1.0)

'''


