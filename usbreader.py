import time

class USBSerialReader:
    """ Read a line from USB Serial (up to end_char), non-blocking, with optional echo """
    def __init__(self):
        self.s = ''  
    def read(self,end_char='\n', echo=True):
        import sys, supervisor
        n = supervisor.runtime.serial_bytes_available
        if n > 0:                    # we got bytes!
            s = sys.stdin.read(n)    # actually read it in
            if echo:
                sys.stdout.write(s)  # echo back to human
            if not s.endswith(end_char):
                self.s = self.s + s      # keep building the string up
            else: # got our end_char!
                rstr = self.s        # save for return
                self.s = ''          # reset str to beginning
                return rstr
        return None                  # no end_char yet

usb_reader = USBSerialReader()

if __name__ == "__main__":
        
    print("type something and press the end_char")
    while True:
        mystr = usb_reader.read()  # read until newline, echo back chars
        #mystr = usb_reader.read(end_char='\t', echo=False) # trigger on tab, no echo
        if mystr:
            print("got:",mystr, end='')
        time.sleep(0.01)  # do something time critical
    
    
    