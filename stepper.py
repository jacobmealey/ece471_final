import RPi.GPIO as GPIO, time

class Motor:
    def __init__(self, step_pin, dir_pin, deg_p_step = 0.225):
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.deg_p_step = deg_p_step
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setwarnings(False)
        GPIO.output(self.step_pin, True)

    def spin(self, steps, direction):
        GPIO.output(self.dir_pin, direction)
        max_speed = 1000
        speed= 30
        while(steps >= 0):
            GPIO.output(self.step_pin, True)
            time.sleep(1.0/speed)
            GPIO.output(self.step_pin, False)
            steps -= 1
            # Ramping logic
            if(speed < max_speed):
                speed += 10
            elif(steps < 50 and speed > 5):
                speed -= 20

    # given a degree (+/- 360) 
    def rotate(self, degrees):
        steps = degrees // self.deg_p_step
        # truncate spins over 360 degrees
        #steps %= 360 // self.deg_p_step 
        self.spin(abs(steps), degrees > 0)
        return (steps * self.deg_p_step)
 


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
