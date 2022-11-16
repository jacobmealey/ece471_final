import RPi.GPIO as GPIO, time

class Motor:
    def __init__(self, step_pin, dir_pin):
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setwarnings(False)
        GPIO.output(self.step_pin, True)

    def spin(self, steps, direction):
        GPIO.output(self.dir_pin, direction)
        while(steps >= 0):
            GPIO.output(self.step_pin, True)
            time.sleep(1/300.0)
            GPIO.output(self.step_pin, False)
            steps -= 1



if __name__=="__main__":
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(3, GPIO.OUT)
    GPIO.output(3, False)
    motor_a = Motor(16, 18)
    motor_b = Motor(24, 26)
    motor_a.spin(200, True)
    time.sleep(0.5)
    motor_a.spin(200, False)
    time.sleep(0.5)

    motor_b.spin(50, True)
    time.sleep(0.5)
    motor_b.spin(50, False)

    GPIO.output(3, True)
    GPIO.cleanup()
