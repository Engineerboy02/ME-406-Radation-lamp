# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 22:18:43 2025

@author: John Lindquist
"""

import serial
import serial.tools.list_ports
import time
from datetime import datetime
import pytz
import sys
import winsound

# Beep settings
frequency = 1500  # Set Frequency To 2500 Hertz
duration = 500  # Set Duration To 1000 ms == 1 second


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def serial_ports():
    # produce a list of all serial ports. The list contains a tuple with the port number, 
    # description and hardware address
    #
    ports = list(serial.tools.list_ports.comports())  

    # return the port if 'USB' is in the description 
    for port_no, description, address in ports:
        if 'USB-SERIAL CH340' in description:
            return port_no
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def serialcreate():
    # Configure serial port settings for serial adapter
    port = serial_ports()  #gets the COM port number

    if not port:
        print("USB COM Port NOT found. Double check connections.")
        Manual = int(input("To try again Hit 1, to enter the com port manualy hit 2, to exit click enter "))

        if (Manual == 1):
            serialcreate()

        elif (Manual == 2):
            comport = str(int(input("please enter the COM Number with out 'COM' (Example: Enter '5' for COM5): ")))
            port = "COM"+comport

        else:
            print("Closing Script")
            time.sleep(5)
            sys.exit()
        
    
    # Configure serial port settings for arduino
    #port = 'COM6'  # Update to your serial port
    baudrate = 115300 # Adjust this if needed
    timeout = .1   # Timeout for serial read/write operations
    serRelay = serial.Serial(port, baudrate, timeout=timeout)

    print()
    print("Serial adapter selected and ready to run")
    print()

    return(serRelay)
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
timebetweenruns = 60 #time delay to let tank drain fully in sec
TankLowValue = 0.690 #Tank Low value for tank drain reset

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def main():
    serRelay = serialcreate()
    inputValues = inputs()
    #serialWrite(inputValues)
    serialGetParmaters(inputValues, serRelay)
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def inputs():

    print()

    LampOntime = float(input("Please enter the lamp on time in sec: ")) #number of secounds to collect data for (starts at 0)
    LampOffTime = float(input("Please enter the lamp off time in sec: "))
    numberofsamples = int(input("Please enter the Number of Samples per trial: ")) #Number of data points within the set time    
    numberofTrials = 1 #int(input("Please enter the Number of Trials: ")) #Number of trials from empty to full

    print()

    #outputFileName = str(input("Please enter the output filename: ")) #output file name the data for all trials just gets appended on the end
    
    inputvalues = [LampOntime, LampOffTime, numberofsamples, numberofTrials] #Puts all the Inputs into and array
    
    print()

    whenReadytoRun = input("Varibles set When ready to run hit enter: ") #Verifys that the user is ready to run the experiment

    return(inputvalues) #returns the Input array to be used in other functions

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def serialGetParmaters(inputValues, serRelay):
    
    #Bulb Pre Warm
    print("Buld Warm up")
    print("Bulb Warming")
    RelayResponse(1, serRelay)

    time.sleep(15)
    print("bulb cooling")
    RelayResponse(0, serRelay)

    time.sleep(15)

    print("Starting trials")
    
    for i in range(inputValues[2]):
        print("Data point", i+1)

        print("Lamp on")
        RelayResponse(1, serRelay)
        time.sleep(inputValues[0]/2)
        print("Beep")
        winsound.Beep(frequency, duration)
        time.sleep(inputValues[0]/2)

        print("Lamp off")
        RelayResponse(0, serRelay)
        time.sleep(inputValues[1])

        print()
        print()

    serRelay.close()

    print()
    print("Current run compleated") #User feed back that the Run was compleated and saved to file
    whatNow = int(input("Hit 1 to run again, or Enter to exit: "))

    if (whatNow == 1):
        print("Script Running again")
        main()
            
    else:
        print("Exiting script and Closing")
        time.sleep(5)
        sys.exit()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def RelayResponse(input, serRelay): #Used to send and receive the serial commands to the PID contoller
    command = [f'0\r\n', f'1\r\n']
    #0 for off
    #1 for 0n

    serRelay.write(command[input].encode())
    CommandResponse = serRelay.read_until('\r').decode('utf-8', errors='ignore').strip()#readline().decode()

    #print(CommandResponse)

    return()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------  
main() #calls the main function
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------