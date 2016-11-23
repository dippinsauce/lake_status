# lake_status

GetConditions == A python script that will provide current temperature and humidity.
  Utilize pigpio to read from DHT22 sensor.  Send RaspberryPi_BCM pin number.
  Wiree sensor to GPIO output to use rebooting function if DHT22 is locked up.

Connections
See table in google drive document.
https://docs.google.com/document/d/1Pi07eDrBE3iylyAJbj9XXQ6EnyEN2k5kweProGx3EXY/edit


Project Scope
*Send temperature to carriots every 30 minutes.  Carriots provides the backend for power
failure / temp too low messaging.

*Read temperature and humidity from dht22 sensor connected to raspberry pi.
*NOT COMPLETE -- Upload readings to database (pythonanywhere.com).
*NOT COMPLETE Develop pythonanywhere screens to plot and trend.
*NOT POSSIBLE (Develop pythonanywhere to provide power off notification with messaging)



