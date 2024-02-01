"""!
@file step_response.py
This file contains code for a step response program using an ADC and timer interrupt.
Contains a function step_response() which measures the time response of the output
voltage at pin B0 in response to a change from 0V to 3.3V at the input at pin C0.
The program prints measurements in two columns, CSV style: the time in
milliseconds since the input step, and the voltage at that time.
The program then plots the data read 

@author Ahren Dosanjh, Jack Krammer, and Lorenzo Pedroza
@date   16-Jan-2024
@copyright (c) 2024 by mecha04 and released under MIT License
"""

import pyb
import micropython
from cqueue import IntQueue

# allows exception messages to be printed
micropython.alloc_emergency_exception_buf(100)

# global variables
QUEUE_SIZE = 200
TIMER_INTERVAL = 10 # 100Hz = 10 ms period
ADC_RESOLUTION = 4096
MAX_VOLTAGE = 3.3
int_queue = IntQueue(QUEUE_SIZE)

# initialize an ADC
adc0 = pyb.ADC(pyb.Pin.board.PB0)

def adc_voltage(adc_val):
    '''!
    Converts Numerical ADC Values to Voltages
    @param      adc_val -> Holds the numerical ADC value
    @return     Returns the voltages of the ADC values
    '''

    return (adc_val / ADC_RESOLUTION) * MAX_VOLTAGE

def timer_int(timer):
    """!
    Timer interrupt function description
    @param      timer -> An object that holds the timer
    @return     None
    """

    # read from adc
    val = adc0.read()

    # add data to queue
    int_queue.put(val)

def print_vals():
    """!
    Prints all values in the int_queue in CSV format
    @param      None
    @return     None
    """
    # intitialize the time variable
    t = 0
    # prints the data in CSV format
    while int_queue.any():
        print('' + str(t) + ',' + str(adc_voltage(int_queue.get())))
        t += TIMER_INTERVAL
    
def step_response(period_ms=10):
    """!
    Step response function description
    @param      period_ms -> Period of the step response in milliseconds
    @return     None
    """

    # calculate the frequency of the period
    f = 1000 // period_ms

    # initialize the output pin
    pc0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)
    
    # initialize a timer to call the interrupt function every 10ms
    tim0 = pyb.Timer(2)
    tim0.init(freq=f, callback=timer_int)

    # turn on pin
    pc0.value(1)

    # check when done getting values
    while not int_queue.full(): 
        continue

    # end timer
    tim0.deinit()

    # turn off pin
    pc0.value(0)

    # make a list with strings in CSV format for every 10 ms
    print_vals()

    # indicate done measuring step response
    print('End')

# The following code only runs if this file is run as the main script;
# it does not run if this file is imported as a module
if __name__ == '__main__':
    step_response(10)


"""
output data:
0,0.1401855
10,0.2336426
20,0.323877
30,0.4084717
40,0.4890381
50,0.5671875
60,0.6429199
70,0.714624
80,0.7847168
90,0.8515869
100,0.9176514
110,0.9796875
120,1.041724
130,1.100537
140,1.158545
150,1.214941
160,1.268115
170,1.320483
180,1.37124
190,1.421191
200,1.468726
210,1.517065
220,1.561377
230,1.605688
240,1.647583
250,1.689478
260,1.729761
270,1.769238
280,1.807104
290,1.844165
300,1.88042
310,1.915063
320,1.948901
330,1.981128
340,2.013355
350,2.044775
360,2.074585
370,2.102783
380,2.132593
390,2.158374
400,2.187378
410,2.213159
420,2.237329
430,2.262305
440,2.285669
450,2.309033
460,2.330786
470,2.353345
480,2.373486
490,2.395239
500,2.414575
510,2.433911
520,2.454053
530,2.470972
540,2.488696
550,2.506421
560,2.522534
570,2.537842
580,2.553149
590,2.568457
600,2.582959
610,2.597461
620,2.611963
630,2.624048
640,2.637744
650,2.65144
660,2.661108
670,2.673193
680,2.686084
690,2.696558
700,2.707837
710,2.718311
720,2.727978
730,2.737646
740,2.74812
750,2.756177
760,2.765845
770,2.774707
780,2.782764
790,2.791626
800,2.799683
810,2.806934
820,2.814184
830,2.821435
840,2.828687
850,2.835132
860,2.841577
870,2.847217
880,2.855273
890,2.859302
900,2.865747
910,2.872192
920,2.873804
930,2.88186
940,2.886694
950,2.891528
960,2.896362
970,2.903613
980,2.90603
990,2.909253
1000,2.914087
1010,2.918921
1020,2.920532
1030,2.925366
1040,2.928589
1050,2.933423
1060,2.937451
1070,2.939062
1080,2.943091
1090,2.945508
1100,2.94873
1110,2.950342
1120,2.95437
1130,2.957593
1140,2.96001
1150,2.964038
1160,2.964844
1170,2.968066
1180,2.971289
1190,2.9729
1200,2.973706
1210,2.976929
1220,2.97854
1230,2.980151
1240,2.983374
1250,2.984985
1260,2.986597
1270,2.989014
1280,2.989819
1290,2.989819
1300,2.993042
1310,2.995459
1320,2.996265
1330,2.996265
1340,2.998682
1350,3.000293
1360,3.001904
1370,3.00271
1380,3.00271
1390,3.005933
1400,3.005933
1410,3.00835
1420,3.007544
1430,3.009155
1440,3.010767
1450,3.012378
1460,3.013184
1470,3.012378
1480,3.014795
1490,3.014795
1500,3.016406
1510,3.019629
1520,3.018823
1530,3.018823
1540,3.018823
1550,3.020435
1560,3.022046
1570,3.02124
1580,3.022851
1590,3.022851
1600,3.027685
1610,3.023657
1620,3.025269
1630,3.025269
1640,3.026074
1650,3.025269
1660,3.027685
1670,3.028491
1680,3.028491
1690,3.030908
1700,3.028491
1710,3.028491
1720,3.030908
1730,3.030908
1740,3.028491
1750,3.031714
1760,3.031714
1770,3.03252
1780,3.034936
1790,3.03252
1800,3.033325
1810,3.033325
1820,3.034131
1830,3.033325
1840,3.034131
1850,3.035742
1860,3.034131
1870,3.038159
1880,3.038159
1890,3.035742
1900,3.035742
1910,3.034936
1920,3.034936
1930,3.037354
1940,3.036548
1950,3.036548
1960,3.038965
1970,3.036548
1980,3.038159
1990,3.038159
End
"""