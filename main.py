#!/usr/bin/python3

import time
import RPi.GPIO as io
from hc_sr04 import Ultrasonic
from stepper import Motor
from sph_to_mesh import write_xyz
import numpy as np

# This function will rotate the motors, recording the angles and the distance as we go.
# returns np array with rho, theta, phi
def spin_routine(ma, mb, us):
    iteration = 0
    step_increment = 5.0
    total_steps = 1600.0
    degrees_per_step = 360 / total_steps
    sample_size = int((180/(step_increment*degrees_per_step)) * (90/(step_increment*degrees_per_step)))
    sample_size = 3*sample_size
    direction_theta = 1
    direction_phi = 1

    rho = []
    theta = []
    phi = []

    rho.append(us.get_distance())
    theta.append(0)
    phi.append(0)

    print(sample_size)
    
    prev_phi = 0
    prev_rho = 0
    prev_the = 0

    while(iteration != sample_size):
        io.output(motor_enable, False)
        # Movement logic - theta always spins from 0 - 360, when 
        # theta changes direction we increment phi which only goes
        # from 0 - 90
        if(prev_the > 360):
            direction_theta = -1
            prev_phi +=  ma.rotate(step_increment * direction_phi)
        elif (prev_the < 0):
            direction_theta = 1
            prev_phi +=  ma.rotate(step_increment * direction_phi)

        if(prev_phi > 90):
            direction_phi = -1
        if(prev_phi < 0):
            direction_phi = 1

        prev_the +=  mb.rotate(step_increment * direction_theta)


        # disable motor for reading sensor -- EMF sad :)
        io.output(motor_enable, True)
        prev_rho = us.get_distance()
        io.output(motor_enable, False)
        # if the distance is over 60 it's in the noise
        if(prev_rho < 50):
            rho.append(prev_rho)
            theta.append(prev_the)
            phi.append(prev_phi)
            print(iteration, rho[-1], theta[-1], phi[-1])
        time.sleep(0.24)
        iteration += 1

    print(len(rho), len(theta), len(phi))
    array = np.array([rho, theta, phi], dtype=float)
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
    io.cleanup()
    io.setup(motor_enable, io.OUT)

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
