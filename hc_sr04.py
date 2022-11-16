#!/usr/bin/python3

import RPi.GPIO as io
import time
import math
import statistics

io.setmode(io.BCM)
trig_pin = 6
echo_pin = 5
io.setup(trig_pin, io.OUT)
io.output(trig_pin, io.LOW)
io.setup(echo_pin, io.IN)

time.sleep(2)

def get_distance():
    
    # trigger for 10 usec
    io.output(trig_pin, True)
    time.sleep(10e-6)
    io.output(trig_pin, False)
 
    t_1 = time.time()
    t_2 = time.time()
 
    # stops recording the time "as soon as" echo goes high 
    while io.input(echo_pin) == 0:
        t_1 = time.time()
 
    # save time of the end of the pulse
    while io.input(echo_pin) == 1:
        t_2 = time.time()
 
    # time difference between start and arrival
    t = t_2 - t_1
    # speed of sound is 34300 cm/s
    distance = (t * 34300) / 2
 
    return distance

def get_distance_interval(tDelay, stat='mean'):
    min_delay = 80e-3
    total_gets = math.ceil(tDelay / min_delay)

    distances = []
    
    for _ in range(total_gets):
        distances.append(get_distance())
        time.sleep(min_delay)
    
    return statistics.mean(distances)




if __name__ == "__main__":

    while True:
        d = get_distance_interval(1)
        print("{} cm".format(d))
