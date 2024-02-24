"""!
@file gui.py
Run real or simulated dynamic response tests and plot the results. This program
demonstrates a way to make a simple GUI with a plot in it. It uses Tkinter, an
old-fashioned and ugly but useful GUI library which is included in Python by
default.

This file is based loosely on an example found at
https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html

@author Jack Krammer and Jason Chang
@date   20-Feb-2024
@copyright (c) 2024 by mecha04 and released under MIT License
"""

import math
import time
import tkinter
from random import random
from serial import Serial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

PORT_NAME = '/dev/tty.usbmodem2055377C39472'
BAUD_RATE = 115200

def get_data():
    '''!
    opens the serial port and reads the data printed to serial. then returns the x and 
    y data as a tuple (x_data_array, y_data_array). 
    @param      None.
    @returns    A tuple of the x data array and y data array in the format (x_data_array,
                y_data_array).
    '''
    print(f'starting to get data')
    # initialize the x and y data arrays
    xdata = []
    ydata = []

    # open the serial port
    with Serial(PORT_NAME, BAUD_RATE) as ser:
        # flush all serial output on this port
        ser.reset_output_buffer()
        # stop the current running program
        ser.write(b'\x03')
        # flush all serial input on this port
        ser.reset_input_buffer()
        # put microcontroller in regualr REPL mode and reboot microcontroller
        ser.write(b'\x02\x04')

        # read the micropython reboot message
        for i in range(6): # should be 6 or 7?-->(7 for all 3 reset codes sent at once)vs(6 for ^C then ^B^D)
            ser.readline()
        # should now be right before any main function print statements
            
        # try writing the input kp value
        ser.write(b'3\n')
        
        # initialize the terminating string
        term_str = 'End'
        # initialize the line read from serial
        data_str = ''
        # read lines from port until 'End'
        while term_str != data_str:
            # read a line from serial
            line = ser.readline()
            # get the data from this line
            data_str = (line[:-2]).decode('ascii')
            data = data_str.split(',')
            # check that there is at least two columns 
            if len(data) >= 2:
                # try to convert data to a float, if error then ignore that line
                try:
                    x = float((data[0]).strip())
                    y = float((data[1]).strip())
                    xdata.append(x)
                    ydata.append(y)
                except:
                    print(f'was not able to convert col 0 = "{(data[0]).strip()}" or col 1 = "{(data[1]).strip()}" to float')
            else:
                print(f'not enough columns of data from line = "{data_str.strip()}"')
        # indicate done reading data
        print(f'reached the terminating string "{term_str}", done reading data.')
    
    # return the tuple of xdata and ydata arrays
    return (xdata,ydata)


def plot_example(plot_axes, plot_canvas, xlabel, ylabel):
    """!
    Make an example plot to show a simple(ish) way to embed a plot into a GUI.
    The data is just a nonsense simulation of a diving board from which a
    typically energetic otter has just jumped.
    @param plot_axes The plot axes supplied by Matplotlib
    @param plot_canvas The plot canvas, also supplied by Matplotlib
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    """
    # Here we create some fake data. It is put into an X-axis list (times) and
    # a Y-axis list (boing). Real test data will be read through the USB-serial
    # port and processed to make two lists like these
    times = [t / 7 for t in range(200)]
    rando = random() * 2 * math.pi - math.pi
    boing = [-math.sin(t + rando) * math.exp(-(t + rando) / 11) for t in times]

    # get the data printed as a result of the main function
    xdata, ydata = get_data()

    # Draw the plot. Of course, the axes must be labeled. A grid is optional
    plot_axes.plot(xdata, ydata)
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    plot_axes.grid(True)
    plot_canvas.draw()


def tk_matplot(plot_function, xlabel, ylabel, title):
    """!
    Create a TK window with one embedded Matplotlib plot.
    This function makes the window, displays it, and runs the user interface
    until the user closes the window. The plot function, which must have been
    supplied by the user, should draw the plot on the supplied plot axes and
    call the draw() function belonging to the plot canvas to show the plot. 
    @param plot_function The function which, when run, creates a plot
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    @param title A title for the plot; it shows up in window title bar
    """
    # Create the main program window and give it a title
    tk_root = tkinter.Tk()
    tk_root.wm_title(title)

    # Create a Matplotlib 
    fig = Figure()
    axes = fig.add_subplot()

    # Create the drawing canvas and a handy plot navigation toolbar
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()

    # Create the buttons that run tests, clear the screen, and exit the program
    button_quit = tkinter.Button(master=tk_root,
                                 text="Quit",
                                 command=tk_root.destroy)
    button_clear = tkinter.Button(master=tk_root,
                                  text="Clear",
                                  command=lambda: axes.clear() or canvas.draw())
    button_run = tkinter.Button(master=tk_root,
                                text="Run Test",
                                command=lambda: plot_function(axes, canvas,
                                                              xlabel, ylabel))

    # Arrange things in a grid because "pack" is weird
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
    toolbar.grid(row=1, column=0, columnspan=3)
    button_run.grid(row=2, column=0)
    button_clear.grid(row=2, column=1)
    button_quit.grid(row=2, column=2)

    # This function runs the program until the user decides to quit
    tkinter.mainloop()


def main():
    '''!
    This function runs when this python file is ran as a main file
    @param      None.
    @returns    None.
    '''
    tk_matplot(plot_example,
               xlabel="Time (ms)",
               ylabel="Position (encoder ticks)",
               title="response of different values for kp gain")


# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program
if __name__ == "__main__":
    main()


