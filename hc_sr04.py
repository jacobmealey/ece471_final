#!/usr/bin/python3

import RPi.GPIO as io
import time
import math
import statistics


class Ultrasonic:
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        # Set up both the trigger and echo pin, sleep to let sensor get ready.
        io.setup(self.trig_pin, io.OUT)
        io.output(self.trig_pin, io.LOW)
        io.setup(self.echo_pin, io.IN)

        time.sleep(2)

    def get_distance(self):
        # trigger for 10 usec
        io.output(self.trig_pin, True)
        time.sleep(10e-6)
        io.output(self.trig_pin, False)
    
        t_1 = time.time()
        t_2 = time.time()
    
        # stops recording the time "as soon as" echo goes high 
        while io.input(self.echo_pin) == 0:
            t_1 = time.time()
    
        # save time of the end of the pulse
        while io.input(self.echo_pin) == 1:
            t_2 = time.time()
    
        # time difference between start and arrival
        t = t_2 - t_1
        # speed of sound is 34300 cm/s
        distance = (t * 34300) / 2
    
        return distance

    def get_distance_mean(self, tDelay, minDelay=80e-3):
        total_gets = math.ceil(tDelay / minDelay)

        distances = []
        
        for _ in range(total_gets):
            distances.append(self.get_distance())
            time.sleep(minDelay)
        
        return statistics.mean(distances)


if __name__ == "__main__":
    trig_pin = 6
    echo_pin = 5

    io.setmode(io.BCM)
    ultrasonic = Ultrasonic(trig_pin, echo_pin)

    while True:
        d = ultrasonic.get_distance_mean(1)
        print("{} cm".format(d))
