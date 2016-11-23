#!/home/pi/lake_status/venv/bin/python

#turn on all heat.  Manual command.
#High heat (raspPi 12, wiringPi 1, broadcomm 18)
#low heat (raspPi 13, wiringPi 2, broadcomm 27)  Model B Rev 2 board  
#get raspberry pi board info from http://www.raspberrypi-spy.co.uk/2012/09/checking-your-raspberry-pi-board-version/

import pigpio

lakepi = pigpio.pi()

try:
    lakepi.write(18, 0)
    lakepi.write(27, 0)
    print("All heat outputs turned Off.")
except:
    print("Something went wrong, outputs may or may not be on")