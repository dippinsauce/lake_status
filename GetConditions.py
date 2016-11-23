#!/home/pi/lake_status/venv/bin/python
"""
SYNOPSIS

    TODO GetConditions [-h,--help] [-v,--verbose] [-u, --upload] [--version]
    
DESCRIPTION

    Gathers temperature/ humidity from DHT22 sensor wired to raspberry pi on "BCM" pin 4.
    Prints or uploads that information to pythonanywhere database OR carriots for power outage notification.

EXAMPLES

    GetConditions    ; read temp/humidity data and print to screen.
    GetConditions -p ; read temp/humidity data and upload to pythonanywhere
    GetConditions -c ; read temp/humidity data and upload to carriots

EXIT STATUS

    (1)  = Exited with failure reading the temp from dht22 (pigpiod daemon not running?)
    (2)  = Exited with failre reading data from dht22 (attempted 20 queries)
    (10) = Exited with failure writing data to pythonanywhere
    (15) = Exited with failure writing data to carriots
    
AUTHOR

    Darrell Webb
    <darrellwebb2<at>gmail.com>

LICENSE

    This script is in the public domain, free from copyrights or restrictions.

VERSION

    0.1 = 5/30/16  First time.
"""

import sys, os, traceback, optparse, logging
import time
import re

import pigpio
import DHT22

import urllib.request, simplejson as json   #required to send data to carriots

def main ():

    global options, args

if __name__ == '__main__':
    
    #initialize logging capability
    loglevel = "INFO"
    logFileName = ("/home/pi/lake_status/GetConditions.log")
    logging.basicConfig(filename=logFileName, level=loglevel,
                        format='%(asctime)s %(levelname)s %(message)s')
    logging.debug("logger started")    

    start_time = time.time()
    parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=globals()['__doc__'], version='$Id$')
    parser.add_option ('-p', '--pythonanywhere', action='store_true', help='sends data to pythonanywhere database')
    parser.add_option ('-c', '--carriots', action='store_true', help='sends data to carriots')
    (options, args) = parser.parse_args()
    
    #get the data from the sensor (pigpiod must be running with root permission)
    logging.debug('trying to get data from dht22')
    try:
        pi = pigpio.pi()
        dht22 = DHT22.sensor(pi, 4)
        #trigger the event, gather the data
        dht22.trigger()
        #check to see if data is relevant, first reading is generally bad, -999 is not right...
        count = 0
    
        while dht22.temperature() > 150 or dht22.temperature() < -20:
            count = count + 1
            #wait 3 seconds and try again.
            logging.debug('bad data from sensor, count : %10o' % count)
            time.sleep(3)
            dht22.trigger()
    	    #error occured, twnety queries to sensor (1min) and no data.
            if count > 20:
                logging.error("Sensor didn't return any data.  Exiting.")
                sys.exit(2)

    #error occured, write to user log and exit.
    except:
        logging.error('lake_status:GetConditions.py failed reading dht22 sensor')
        sys.exit(1)
    
    #print to screen and exit cleanly.
    
    logging.debug("GetConditions.py called, verbose output")
    print(time.asctime())
    logging.debug('timeasctime :' + time.asctime())
    print('Current temperature : %5.2f deg C' % dht22.temperature())
    logging.debug('Current temperature : %5.2f deg C' % dht22.temperature())
    print('Current humidity : %5.2f %%' % dht22.humidity())
    logging.debug('Current humidity : %5.2f %%' % dht22.humidity())
    print('TOTAL TIME IN SECONDS: %5.3f' % (time.time() - start_time))
    logging.debug('TOTAL TIME IN SECONDS: %5.3f' % (time.time() - start_time))
    
    #upload to pythonanywhere
    if options.pythonanywhere:
        logging.debug("GetConditions.py called; pythonanywhere upload")
        try:
            sys.exit(0)
            #send data to pythonanywhere database
            #Database host address:dippinsauce.mysql.pythonanywhere-services.com
            #Username:dippinsauce
        
        #problem uploading to pythonanywhere, write to user log and exit.
        except:
            logging.error('lake_status:GetConditions.py failed writing to pythonanywhere')
            sys.exit(10)
    
    ''' Get data to Carriots '''
    if options.carriots:
        logging.debug("GetConditions.py called; carriots upload")
        #try:
            #Carriots information for LakePi
        API_KEY = "335bfc7b68243ee3663e7370fdbc370e883c2f398630aeff0525648fadd8e12b"
        DEVICE = "LakePi@dippinsauce"
        
        #Setup class for communicating to Carriots.com
        class Client(object):
            api_url = "http://api.carriots.com/streams"  
            
            def __init__(self, api_key = None, client_type = 'json'):
                self.client_type = client_type
                self.api_key = api_key
                self.content_type = "application/vnd.carriots.api.v2+%s" % (self.client_type)
                self.headers = {'User-Agent': 'Raspberry-Carriots',
                             'Content-Type': self.content_type,
                             'Accept': self.content_type,
                             'Carriots.apikey': self.api_key}
            
            def send(self, data):
                self.data = json.dumps(data)
                logging.debug("here is the json.dumps -----")
                logging.debug(self.data)
                self.data = self.data.encode()
                logging.debug("here is the json.dumps after encode -----")
                logging.debug(self.data)
                request = urllib.request.Request(Client.api_url, self.data, self.headers)
                self.response = urllib.request.urlopen(request)
                return self.response
        
        #send data to carriots
        #Example taken from https://www.carriots.com/tutorials/Arduino_RPi_Carriots/flowmeter#raspberry_code
        client_carriots = Client(API_KEY)
        tempF = ((dht22.temperature() *9)/5) + 32    #convert to deg F
        
        logging.info("Temp = %s -- Humidity = %s", tempF, dht22.humidity())
        
        data = {"protocol":"v2","device":DEVICE,"at":"now",
                  "data":{"temperature": tempF, "humidity": dht22.humidity()}}

        logging.debug("Sending data to Carriots.com == Sending --")
        logging.debug(data)
        carriots_response = client_carriots.send(data)
        
        logging.debug("Sending data to Carriots.com == Response --")
        logging.debug(carriots_response.read())
        
        #except:
        #    logging.error("lake_status;GetConditions.py failed writing to carriots")
        #    sys.exit(15)
            
