import serial
from matplotlib import pyplot as plt
import numpy as np
import time

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
fig = plt.figure(figsize=(h, w)) # setting to 14x8 to approximate fullscreen
# fig = plt.figure()

plt.rcParams['toolbar'] = 'None' # Remove tool bar (upper bar)
fig.canvas.window().statusBar().setVisible(False) # Remove status bar (bottom bar)


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

# from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
# def _update_buttons_checked(self):
    # print("::", self._actions)
    # # sync button checkstates to match active mode (patched)
    # if 'pan' in self._actions:
        # self._actions['pan'].setChecked(self._active == 'PAN')
    # if 'zoom' in self._actions:
        # self._actions['zoom'].setChecked(self._active == 'ZOOM')
# NavigationToolbar2QT._update_buttons_checked = _update_buttons_checked

# ~ toolbar = plt.get_current_fig_manager().toolbar
# ~ print(toolbar.__dir__())
# ~ plt.rcParams['toolbar'] = 'toolbar2'
# ~ print(plt.rcParams)
# ~ toolbar.isActive = False
# ~ for x in toolbar.actions():
    # ~ 
    # ~ exit()s


def updateGraph(lijst):
	
	# change the range on the Y axis
	minimum = min(lijst)-1000
	if minimum < 0:
		minimum = 0
	ax.set_ylim(minimum, max(lijst)+1000)

	# add the new data to the graph
	line.set_data(x, lijst)
	
	fig.canvas.draw()

	fig.canvas.flush_events()

# Connect the close event to the on_close function
fig.canvas.mpl_connect('close_event', on_close)

plt.show(block=False)

# begin een lijst voor recente waardes door een array te vullen met een standaardwaarde
lijst = np.full(100, 8000) # lijst van alle data die we ontvangen hebben
# laat de grafiek vast zien, ook als er nog geen nieuwe data binnenkomt
fig.canvas.draw()
fig.canvas.flush_events()
updateGraph(lijst)

# Main loop
while True:
    
    try:
        # Read a line from the serial port
        data = ser.readline().decode('utf-8').strip()
        data = int(data)

        # add the new data to the list (and remove a line from the top)
        lijst = np.roll(lijst, -1)
        lijst[-1] = data

        updateGraph(lijst)
        
    except: # als er geen data binnenkomt maar een status message, 
        # print dan de message en wacht op nieuwe waardes
        print(data)
        data = ser.readline().decode('utf-8').strip()
