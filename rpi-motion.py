# Use HC-SR501 for motion detection to start browser / video

import RPi.GPIO as GPIO
import time
import subprocess

# Configuration Parameters
MOTION_SCREEN_NUMBER = 1  # Screen number for motion detection
MOTION_BROWSER_COMMAND = "chromium-browser"  # Command to start the web browser
MOTION_BROWSER_URL = "http://your-website-url"  # URL to open in the web browser
MOTION_PLAYLIST_PATH_2 = "home/otto/11.xspf"  # Path to motion detection playlist when no motion is detected
FAILSAFE_THRESHOLD = 30  # Time threshold in seconds for the fail-safe mechanism

# Configure GPIO pin
GPIO_MOTION = 23

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_MOTION, GPIO.IN)

def start_browser_fullscreen():
    browser_command = [
        MOTION_BROWSER_COMMAND,
        "--kiosk",
        MOTION_BROWSER_URL
    ]
    subprocess.run(browser_command)

def start_vlc_random_video(playlist, screen_number):
    vlc_command = [
        "vlc",
        "--playlist-autostart",
        "--fullscreen",
        "--screen-number",
        str(screen_number),
        "--random"
    ]
    vlc_command.extend(subprocess.check_output(["cat", playlist]).decode().splitlines())
    subprocess.run(vlc_command)

def motion_detected():
    print("Motion detected!")
    start_browser_fullscreen()

def no_motion_detected():
    print("No motion detected!")
    time.sleep(0.1)

    # Fail-safe mechanism
    no_motion_detected_start_time = time.time()
    while time.time() - no_motion_detected_start_time <= FAILSAFE_THRESHOLD:
        if GPIO.input(GPIO_MOTION) == GPIO.HIGH:
            print("Motion re-detected during fail-safe delay. Waiting for true no motion state.")
            break
        time.sleep(0.1)
    else:
        # Start the second playlist after the fail-safe time
        start_vlc_random_video(MOTION_PLAYLIST_PATH_2, MOTION_SCREEN_NUMBER)

if __name__ == '__main__':
    try:
        while True:
            if GPIO.input(GPIO_MOTION) == GPIO.HIGH:
                motion_detected()
            else:
                no_motion_detected()

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Motion detection stopped by User")
        GPIO.cleanup()
