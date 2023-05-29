# Use HC-SR501 for motion detection

import RPi.GPIO as GPIO
import time

# Configure GPIO pin
GPIO_PIR = 23  # GPIO pin for PIR motion sensor

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIR, GPIO.IN)

def motion_detected():
    print("Motion detected!")
    # Add your custom code here for when motion is detected

def no_motion_detected():
    print("No motion detected!")
    # Add your custom code here for when no motion is detected

def motion_detection():
    while True:
        if GPIO.input(GPIO_PIR):
            motion_detected()
        else:
            no_motion_detected()

        time.sleep(0.1)

if __name__ == '__main__':
    try:
        motion_detection()

    except KeyboardInterrupt:
        print("Motion detection stopped by User")
        GPIO.cleanup()
