#turn on all heat.  Manual command.
#High heat (raspPi 12, wiringPi 1, broadcomm 18)
#low heat (raspPi 13, wiringPi 2, broadcomm 27)  Model B Rev 2 board  
#get raspberry pi board info from http://www.raspberrypi-spy.co.uk/2012/09/checking-your-raspberry-pi-board-version/

import pigpio

pi = pigpio.pi()

try:
    pi.write(18, 1)
    pi.write(27, 1)
    print("All heat outputs turned on.")
except:
    print("Something went wrong, outputs may or may not be on")