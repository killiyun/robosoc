import os, time, threading, queue
import RPi.GPIO as GPIO

## startup ------------------------------------------------------

os.system("sudo pigpiod")
time.sleep(1)  # do not remove apparently
import pigpio

GPIO.setmode(GPIO.BCM)
sonic_sensors = {"front": (2, 3), "left": (4, 17), "right": (27, 22)}

ESC1 = 18  # Connect the ESC in this GPIO pin
ESC2 = 24  # Connect the ESC of second motor to this GPIO pin

pi = pigpio.pi()
pi.set_servo_pulsewidth(ESC1, 0)
pi.set_servo_pulsewidth(ESC2, 0)

state = 0

for pin_tuple in sonic_sensors.values():
    GPIO.setup(pin_tuple[0], GPIO.OUT)
    GPIO.setup(pin_tuple[1], GPIO.IN)


max_value = 2000
min_value = 1000

# get distance function -------------------------------------

def check_distance(pin, q):
    while True:
        GPIO.output(sonic_sensors[pin][0], True)
        time.sleep(0.00001)
        GPIO.output(sonic_sensors[pin][0], False)
        StartTime = time.time()
        StopTime = time.time()

        while GPIO.input(sonic_sensors[pin][1]) == 0:
            StartTime = time.time()

        while GPIO.input(sonic_sensors[pin][1]) == 1:
            StopTime = time.time()

        q.append((StopTime - StartTime) * 34300 / 2)
        time.sleep(0.001)

def change_state(f, l, r):
    # no clue what happens if theres nothing on the queue, probably just None
    fdist = f[0]
    ldist = l[0]
    rdist = r[0]

    if fdist and fdist <= 150:
        # belt forwards but not full speed if it sees something in front
        state = 0
        f.remove(f[0])
        if ldist:
            l.remove(l[0])
        if rdist:
            r.remove(r[0])

    if (rdist or ldist)
        # spot out of corner of eye

def state_1():
    # oh no


# start of program -----------------------------------------

if __name__ == "__main__":
    try:
        # set up sensor threads
        front_queue = [];
        left_queue = [];
        right_queue = [];
        front_distance_thread = threading.Thread(target=check_distance, args=("front", front_queue))
        left_distance_thread = threading.Thread(target=check_distance, args=("left", left_queue))
        right_distance_thread = threading.Thread(target=check_distance, args=("right", right_queue))
        front_distance_thread.start()
        left_distance_thread.start()
        right_distance_thread.start()


        """
        pi.set_servo_pulsewidth(ESC1, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC1, max_value)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC1, min_value)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC1, 1500)
        pi.set_servo_pulsewidth(ESC2, 1500)
        state = 0
        while True:

            if state == 0:
                fuck_off()
            elif state == 1:
                offset()
            elif state == 2:
                blind()
            elif state == 3:
                smash()

            dist = distance("front")
            print(dist)
            if dist <= 150:
                pi.set_servo_pulsewidth(ESC1, 1600)
                pi.set_servo_pulsewidth(ESC2, 1600)
            else:
                pi.set_servo_pulsewidth(ESC1, 1500)
                pi.set_servo_pulsewidth(ESC2, 1500)
            time.sleep(0.5)
        """
    except KeyboardInterrupt:
        GPIO.cleanup()
        os.system("sudo killall pigpiod")
        pi.stop()
