import threading
import serial.tools.list_ports
import serial

def read_serial_data(serial_port, unique_id):
    while True:
        try:
            data = serial_port.readline().decode('utf-8').strip()
            if data:
                print(f"Pico {unique_id}: {data}")
        except serial.SerialException:
            print(f"Fout bij lezen van data op microcontroller {serial_port.port}")
            break

def setup_serial_connection(port, baudrate=9600):
    try:
        serial_port = serial.Serial(port, baudrate)
        return serial_port
    except serial.SerialException:
        print(f"Fout bij het opzetten van de seriële verbinding op poort {port}")
        return None

def discover_microcontrollers():
    ports = list(serial.tools.list_ports.comports())
    return [port.device for port in ports]

def get_microcontroller_id(serial_port):
    try:
        serial_port.write(b"GET_ID_COMMAND\r\n")  # Stuur een commando om het ID op te vragen
        response = serial_port.readline().decode('utf-8').strip()
        return response
    except serial.SerialException:
        print(f"Fout bij het verkrijgen van het ID van microcontroller {serial_port.port}")
        return None
    
def main():
    print("see if there are any Pico's connected")
    microcontroller_ports = discover_microcontrollers()

    if not microcontroller_ports:
        print("Geen microcontrollers gevonden.")
        return

    threads = []
    
    number_of_Picos = len(microcontroller_ports) # to fake unique id's that will be self-reported by the Pico's

    for port in microcontroller_ports:
        serial_port = setup_serial_connection(port)
        if serial_port:
            number_of_Picos -= 1
            # ~ unique_id = get_microcontroller_id(serial_port) # deze handshake moet nog aangezet woden op de Pico's 
            unique_id = number_of_Picos
            if unique_id:
                print(f"Uniek ID van microcontroller op poort {serial_port.port}: {unique_id}")
                thread = threading.Thread(target=read_serial_data, args=(serial_port, unique_id), daemon=True)
                thread.start()
                threads.append(thread)
                

    # Wacht totdat de gebruiker het script stopt
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Script gestopt.")

        # Sluit alle threads en seriële verbindingen
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    main()
