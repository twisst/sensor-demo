import serial
from matplotlib import pyplot as plt
import numpy as np

from startSerialConnection import *
ser = startSerialConn()

from getScreenSize import *
h, w = screenSize(1280,1024)

def on_close(event):
    print("Matplotlib window closed.")
    plt.close()
    exit()
    # Add any cleanup or additional actions you want to perform before exiting

# setting this to fullscreen works well with agg backend, but on MacOSX backend running in fullscreen makes matplotlib awfully slow) 
manager = plt.get_current_fig_manager()
# manager.full_screen_toggle() 

x = np.linspace(0,25, num=100)
# fig = plt.figure(figsize=(h, w)) # setting to 14x8 to approximate fullscreen
fig = plt.figure(1)
fig.set_facecolor("xkcd:dark green") # altenative: "#282828"
ax = fig.add_subplot(1, 1, 1)
ax.set(facecolor="xkcd:dark green")

line, = ax.plot([])
plt.setp(line, color="#66FF66", linewidth=2.0)
text = ax.text(0.8,0.5, "")

# Remove ticks along the x-axis
# ax.set_xticks([])

ax.set_xlim(x.min(), x.max())

plt.grid(visible=True, axis='both', color='#409040', linestyle='--', linewidth=0.8)

# Connect the close event to the on_close function
fig.canvas.mpl_connect('close_event', on_close)

plt.show(block=True)

# get a first value from the Pico
waarde = int(ser.readline().decode('utf-8').strip())
# begin een lijst met recente waardes door een array te vullen met die eerste waarde
lijst = np.full(100, waarde) # lijst van alle data die we ontvangen hebben

# Main loop
while True:
    
    # Read a line from the serial port
    data = int(ser.readline().decode('utf-8').strip())
    
    # add the new data to the list (and remove a line from the top)
    lijst = np.roll(lijst, -1)
    lijst[-1] = data

    # change the range on the Y axis
    minimum = min(lijst)-1000
    if minimum < 0:
        minimum = 0
    ax.set_ylim(minimum, max(lijst)+1000)

    # add the new data to the graph
    line.set_data(x, lijst)
    
    fig.canvas.draw()

    fig.canvas.flush_events()
