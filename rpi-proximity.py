# Use HC-SR04+ sensor to measure distance with Raspberry Pi and run some actions

import RPi.GPIO as GPIO
import time
import subprocess
import random

# Configuration Parameters
VIDEO_PATH_1 = "file:///path/to/file"  # Path to video 1
VIDEO_PATH_2 = "file:///path/to/file"  # Path to video 2
VIDEO_PATH_3 = "file:///path/to/file"  # Path to video 3
VIDEO_PATH_4 = "file:///path/to/file"  # Path to video 4
VIDEO_PATH_5 = "file:///path/to/file"  # Path to default video
PROXIMITY_THRESHOLD = 200  # Proximity threshold in centimeters
PROXIMITY_TIMEOUT = 33 # Timeout in seconds

# Configure GPIO pins
GPIO_TRIGGER = 19  # GPIO pin for proximity sensor trigger
GPIO_ECHO = 26  # GPIO pin for proximity sensor echo

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)

proximity_detected_time = 0
vlc_process = None
is_playing_video = False

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    start_time = time.time()
    stop_time = time.time()

    # save start time
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # time difference between start and arrival
    time_elapsed = stop_time - start_time
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (time_elapsed * 34300) / 2

    return distance

def start_vlc_video_fullscreen_random(video):
    global vlc_process
    if vlc_process is not None:
        vlc_process.kill()
        vlc_process.wait()
    vlc_command = [
        "cvlc",
        "--fullscreen",
        video
    ]
    vlc_process = subprocess.Popen(vlc_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def on_proximity_detected():
    global proximity_detected_time, is_playing_video
    print("Proximity detected!")
    if not is_playing_video:
        proximity_detected_time = time.time()
        random_video = random.choice([VIDEO_PATH_1, VIDEO_PATH_2, VIDEO_PATH_3, VIDEO_PATH_4])
        start_vlc_video_fullscreen_random(random_video)
        is_playing_video = True
        print("Start random")

def on_no_proximity_detected():
    global is_playing_video
    print("No proximity detected!")
    # Keep playing VIDEO_PATH_5
    print("Playing default video")

def proximity_detection():
    global proximity_detected_time, is_playing_video

    while True:
        if distance() < PROXIMITY_THRESHOLD:
            on_proximity_detected()
        elif is_playing_video:
            elapsed_time = time.time() - proximity_detected_time
            if elapsed_time >= PROXIMITY_TIMEOUT:
                on_no_proximity_detected()
        else:
            on_no_proximity_detected()

        time.sleep(0.1)


if __name__ == '__main__':
    try:
        proximity_detection()

    except KeyboardInterrupt:
        print("Proximity detection stopped by User")
        GPIO.cleanup()
