# deze versie gebruikt blit om de grafiek te tonen. 
# dat is sneller dan gewoon fig.canvas.draw(), 
#   maar met die aanpak kunnen we geen dynamische range laten zien.
# op de snelheid waarmee we nu data van de Pico naar de Pi willen sturen merk je echter niks van dat verschil in snelheid. (70ms)


import serial
import time
from matplotlib import pyplot as plt
import numpy as np

from startSerialConnection import *
ser = startSerialConn()


x = np.linspace(0,50., num=100)
fig = plt.figure()
fig.set_facecolor("xkcd:dark green") # altenative: "#282828"
ax = fig.add_subplot(2, 1, 2)
ax.set(facecolor="xkcd:dark green")



# Toggle fullscreen mode
fig.canvas.manager.full_screen_toggle() # toggle fullscreen mode
# plt.get_current_fig_manager().full_screen_toggle() # toggle fullscreen mode


line, = ax.plot([])
plt.setp(line, color="#66FF66", linewidth=2.0)
text = ax.text(0.8,0.5, "")

# Remove ticks along the x-axis
# ax.set_xticks([])

ax.set_xlim(x.min(), x.max())

plt.grid(visible=True, axis='both', color='#409040', linestyle='--', linewidth=0.8)

fig.canvas.draw()   # note that the first draw comes before setting data 

# cache the background
ax_background = fig.canvas.copy_from_bbox(ax.bbox)

plt.show(block=False)

t_start = time.time()

i=0 # for calculating FPS

lijst = np.zeros(100)

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
    
    # show FPS
    # i += 1
    # tx = 'Mean Frame Rate:\n {fps:.3f}FPS'.format(fps= ((i+1) / (time.time() - t_start)) ) 
    # text.set_text(tx)
    #print tx

    # restore background
    fig.canvas.restore_region(ax_background)

    # redraw just the points
    ax.draw_artist(line)
    ax.draw_artist(text)

    # fill in the axes rectangle
    fig.canvas.blit(ax.bbox)

    fig.canvas.flush_events()
