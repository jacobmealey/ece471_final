#!/usr/bin/python3

import time
import RPi.GPIO as io
from hc_sr04 import Ultrasonic
from stepper import Motor

# This function will rotate the motors, recording the angles and the distance as we go.
def spin_routine():
    pass


if __name__ == "__main__":
    trig_pin = 6
    echo_pin = 5

    motor_a_step_pin = 16
    motor_a_dir_pin = 18
    motor_b_step_pin = 24
    motor_b_dir_pin = 26

    io.setmode(io.BCM)

    motor_a = Motor(motor_a_step_pin, motor_a_dir_pin)
    motor_b = Motor(motor_b_step_pin, motor_b_dir_pin)
    ultrasonic = Ultrasonic(trig_pin, echo_pin)
