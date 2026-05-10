from microbit import *
import music
import speech
import struct

## Initial settings
# Stop the right motor
pin13.write_analog(511)
# Stop the left motor
pin14.write_analog(511)
# Set the period of the signal sent to the right motor to 1 second
pin13.set_analog_period(1000)
# Set the period of the signal sent to the left motor to 1 second
pin14.set_analog_period(1000)
# Release the brake on the right motor
pin15.write_digital(0)
# Release the brake on the left motor
pin16.write_digital(0)
# Left turn flag
left_turn = 0
# Right turn flag
right_turn = 0

# Ultrasonic sensor address
address = 0
# reflection time
reflection_time = 0
# Reflection time (higher digits)
reflection_time_h = 0
# Reflection time (lower digits)
reflection_time_l = 0
# Ultrasonic sensor response
response = 0
# reflection distance
reflaction_distance = 0
# Distance to the obstacles
distance = 0


# Check the distance to the obstacle
def get_distance_from_obstacles():
    global address, distance
    address = 0x2C
    distance = 0
    conn_i2c()
    # When the distance to the obstacle is within 100cm
    if 0 <= reflaction_distance and reflaction_distance <= 1000:
        # Round the reflection distance to the nearest whole number and set it to the distance to the obstacle
        distance = round(reflaction_distance)
    else:
        # Reset the distance to the obstacle
        distance = 0


# Connect to the ultrasonic sensor via I2C
def conn_i2c():
    global reflection_time, reflection_time_h, reflection_time_l, response, reflaction_distance
    reflection_time = 0
    reflection_time_h = 0
    reflection_time_l = 0
    response = 0
    reflaction_distance = 0
    # If the ultrasonic sensor does not start or does not return a correct result, repeat the process
    while response == 0 or (reflection_time_h == 0 and reflection_time_l == 0):
        # Send the value 51 to the ultrasonic sensor (address: 44) and start using it
        command_51 = struct.pack(">B", 51)
        i2c.write(address, bytearray(command_51), False)
        sleep(100)
        # Get a response from the ultrasonic sensor
        response = int.from_bytes(i2c.read(address, 1, False), "big")
        # If the sensor is successfully started
        if response == 1:
            # Send the value 16 to address 44 and perform the operation of obtaining the sum of the higher and lower digits of the reflection time
            command_16 = struct.pack(">B", 16)
            i2c.write(address, bytearray(command_16), False)
            sleep(100)
            # Get the sum of the higher and lower digits of the firing time
            reflection_time = int.from_bytes(i2c.read(address, 1, False), "big")
            # Send the value 15 to address 44 and retrieve the reflection time (higher digits)
            command_15 = struct.pack(">B", 15)
            i2c.write(address, bytearray(command_15), False)
            sleep(100)
            # Get the reflection time (higher digits)
            reflection_time_h = int.from_bytes(i2c.read(address, 1, False), "big")
            # Send the value 14 to address 44 and retrieve the reflection time (lower digits)
            command_14 = struct.pack(">B", 14)
            i2c.write(address, bytearray(command_14), False)
            sleep(100)
            # Get the reflection time (lower digits)
            reflection_time_l = int.from_bytes(i2c.read(address, 1, False), "big")
            # If the sum of the higher and lower digits of the reflection time is incorrect
            if reflection_time != reflection_time_h + reflection_time_l:
                # Reset the reflection time
                reflection_time_h = 0
                reflection_time_l = 0
            else:
                # The reflection distance can be obtained from the reflection time using the following method
                # 1. Multiply the higher digit by 256 to convert to decimal, add it to the lower digit, and subtract the ultrasonic sensor noise correction value: 160
                # 2. Divide the result no.1 by 2 to calculate the one-way reflection time
                # 3. Multiply the result no.2 by the speed of ultrasound: 0.315 (mm/μs) to calculate the reflection distance
                reflaction_distance = (
                    (reflection_time_h * 256 + reflection_time_l - 160) / 2 * 0.315
                )


### メインプログラム
while True:
    # Stop the right motor
    pin13.write_analog(511)
    # Stop the left motor
    pin14.write_analog(511)
    # Play the built-in music
    if left_turn == 0 and right_turn == 0:
        music.play(music.ENTERTAINER, pin=pin8, wait=True, loop=False)
    else:
        music.play(music.BA_DING, pin=pin8, wait=True, loop=False)
    sleep(1000)
    # Check the distance to the obstacle
    get_distance_from_obstacles()
    sleep(1000)
    # If the distance to the obstacle is within 10 cm
    if 0 < distance and distance < 100:
        # Stop the right motor
        pin13.write_analog(511)
        # Stop the left motor
        pin14.write_analog(511)
        # Output audio
        speech.say("Detect obstacles", speed=120, pitch=50, throat=50, mouth=200)
        sleep(1000)
        # Play the built-in music
        music.play(music.DADADADUM, pin=pin8, wait=True, loop=False)
        sleep(1000)
        # Show anger mark
        display.show(Image.ANGRY)
        sleep(1000)
    # Turn left three times
    elif left_turn < 3:
        # Turn the right motor
        pin13.write_analog(1023)
        # Turn the left motor
        pin14.write_analog(1023)
        sleep(2000)
        # Output audio
        speech.say("Turn Left", speed=120, pitch=50, throat=50, mouth=200)
        sleep(1000)
        # Show left arrow
        display.show(Image.ARROW_E)
        sleep(1000)
        # Turn the right motor
        pin13.write_analog(1023)
        # Turn the left motor
        pin14.write_analog(0)
        sleep(1790)
        # Count up the left turn flag
        left_turn += 1
    # Run diagonally and turns to the right
    elif left_turn == 3:
        # Turn the right motor
        pin13.write_analog(1023)
        # Turn the left motor
        pin14.write_analog(1023)
        sleep(8000)
        # Output audio
        speech.say("Turn Right", speed=120, pitch=50, throat=50, mouth=200)
        sleep(1000)
        # Show right arrow
        display.show(Image.ARROW_W)
        sleep(1000)
        # Turn the right motor
        pin13.write_analog(0)
        # Turn the left motor
        pin14.write_analog(1023)
        sleep(1790)
        # Count up the left turn flag
        left_turn += 1
    # Turn right three times
    elif right_turn < 2:
        # Turn the right motor
        pin13.write_analog(1023)
        # Turn the left motor
        pin14.write_analog(1023)
        sleep(2000)
        # Output audio
        speech.say("Turn Right", speed=120, pitch=50, throat=50, mouth=200)
        sleep(1000)
        # Show right arrow
        display.show(Image.ARROW_W)
        sleep(1000)
        # Turn the right motor
        pin13.write_analog(0)
        # Turn the left motor
        pin14.write_analog(1023)
        sleep(1790)
        # Count up the right turn flag
        right_turn += 1
    # Run to the starting point
    else:
        # Turn the right motor
        pin13.write_analog(1023)
        # Turn the left motor
        pin14.write_analog(1023)
        sleep(4000)
        # Reset the flag
        left_turn = 0
        right_turn = 0
