#!/usr/bin/python3

import time
import RPi.GPIO as io
from hc_sr04 import Ultrasonic
from stepper import Motor
from sph_to_mesh import write_xyz
import numpy as np

# This function will rotate the motors, recording the angles and the distance as we go.
# returns np array with rho, phi and rad
def spin_routine(ma, mb, us):
    iteration = 0
    step_increment = 10
    direction_rho = 1
    direction_phi = 1

    rho = []
    phi = []
    rad = []

    rho.append(0)
    phi.append(0)
    rad.append(us.get_distance())

    while(iteration != 100):
        rad.append(us.get_distance())
        rho.append(rho[-1] + mb.rotate(step_increment * direction_rho))
        phi.append(phi[-1])
        print(iteration, rho[-1], phi[-1], rad[-1])

        if(rho[-1] > 180 or rho[-1] < 0):
            direction_rho *= -1
            phi.append(phi[-1] + ma.rotate(step_increment * direction_phi))
            rho.append(rho[-1] + mb.rotate(step_increment * direction_rho))
            rad.append(us.get_distance())

        if(phi[-1] > 180 or phi[-1] < 0):
            direction_phi *= -1

        iteration += 1

    print(len(rho), len(phi), len(rad))
    array = np.array([rho, phi, rad], dtype=float)
    return array.T


if __name__ == "__main__":
    trig_pin = 6
    echo_pin = 5

    motor_a_step_pin = 23
    motor_a_dir_pin = 24
    motor_b_step_pin = 8 
    motor_b_dir_pin = 7 
    motor_enable = 2

    io.setmode(io.BCM)
    io.setup(motor_enable, io.OUT)
    io.output(motor_enable, False)

    time.sleep(0.5)

    motor_a = Motor(motor_a_step_pin, motor_a_dir_pin)
    motor_b = Motor(motor_b_step_pin, motor_b_dir_pin)
    ultrasonic = Ultrasonic(trig_pin, echo_pin)
    print(ultrasonic.get_distance())

    array = spin_routine(motor_a, motor_b, ultrasonic)
    #np.savetxt("test.csv", array, delimiter=",")
    write_xyz("test.xyz", array)

    io.output(motor_enable, True)
    io.cleanup()
