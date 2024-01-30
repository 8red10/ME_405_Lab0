"""!
@file square.py
This file contains code that produces a square wave.

TODO: Write a script in main.py which sets pin C0 as an output, then runs a loop in
which C0 is at logic 0 for 5 seconds, then logic 1 for 5 seconds, and repeats until
Ctrl-C is pressed.

@author Ahren Dosanjh, Jack Krammer, and Lorenzo Pedroza
@date   16-Jan-2024
@copyright (c) 2024 by mecha04 and released under MIT License
"""

import pyb
import utime

def main():
    """!
    Outputs a square wave on pin PC0 with 10 second period
    @param      None
    @return     None
    """

    # Set up PC0
    pc0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)

    # Infinite while loop
    while True:
        # PC0 set to high
        pc0.value(1)
        
        # Wait 5 seconds
        utime.sleep_ms(5000)
        
        # PC0 set to low
        pc0.value(0)
        
        # Wait 5 seconds
        utime.sleep_ms(5000)

# The following code only runs if this file is run as the main script;
# it does not run if this file is imported as a module
if __name__ == '__main__':
    main()
