
# find the actual port the Raspberry Pi Pico is connected to
import serial.tools.list_ports

def startSerialConn():
    
    # Get a list of all available serial ports
    ports = serial.tools.list_ports.comports()
    usbmodem_ports = []
    for port in ports:
        # print(f"Port: {port.device}, Description: {port.description}, Hardware ID: {port.hwid}")
        if "USB" in port.hwid:
            usbmodem_ports.append(port.device) 
            serial_port = port.device
    if usbmodem_ports:
        print("USB modem ports found:")
        for port in usbmodem_ports:
            print(port)
    else:
        print("No USB modem ports found.")
        exit()

    # Create a serial connection
    baud_rate = 115200
    # serial_port = '/dev/tty.usbmodem14201'
    ser = serial.Serial(serial_port, baud_rate)
    
    return ser
