# —-----------------------------------------------------
# Comp 9 Term 2 Project - Traffic Light Crossing
# By Evan Prael, Feb 20, 2023
#
# This program runs on a Raspberry Pi and controls LEDs, a buzzer, 
# and more to show what happens when a crosswalk button is pressed.  
#
# Useful links:
#
#  - A video of the running code and hardware
#  - This code on Github
#  - GPIO reference and tutorials
#  - Sample traffic light code (bottom of page)
#  - Google Code Blocks for coloring source code in Google Docs
# —-----------------------------------------------------

# libraries for clearing the screen, time delays, and GPIO pins
import os
import time
from gpiozero import Button, LED, Buzzer,LEDCharDisplay


os.system("")




# ASSIGNING PINS
#-------------------------------------------------------------

# traffic light
traffic_red = LED(25)
traffic_yellow = LED(8)
traffic_green = LED(7)

# crosswalk light
cross_red=LED(14)
cross_white=LED(18)

# button and buzzer
button = Button(24)
buzzer = Buzzer(15)

# digital display
# 7 pins for seven LEDs
display = LEDCharDisplay(26, 19, 13, 6, 5, 21, 20, active_high=True)


# FUNCTIONS
#-------------------------------------------------------------


# turn everything off
#-------------------------------------------------------------
def reset_all():
    buzzer.off()
    traffic_red.off()
    traffic_yellow.off()
    traffic_green.off()
    cross_red.off()
    cross_white.off()


# play buzzer 
#-------------------------------------------------------------
def play_buzzer(seconds):
    print ("playing buzzer")
    buzzer.on()
    time.sleep (seconds)
    buzzer.off()



# set traffic light color 
# if blink == true, blinks 1/2 second on, 1/2 second off
#-------------------------------------------------------------
def set_trafficlight (color, blink):
    traffic_red.off()
    traffic_yellow.off()
    traffic_green.off()
    print ("setting traffic light to " + color)

    if (blink == True):
        if (color == "yellow"):
            traffic_yellow.blink(0.5,0.5)
        if (color=="green"):
            traffic_green.blink(0.5,0.5)
        if (color=="red"):
            traffic_red.blink(0.5,0.5)
    else:
        if (color == "yellow"):
            traffic_yellow.on()
        if (color=="green"):
            traffic_green.on()
        if (color=="red"):
            traffic_red.on()
      
# set crosswalk light color 
# if blink == true, blinks 1/2 second on, 1/2 second off
#-------------------------------------------------------------
def set_crosswalklight (color, blink):
    cross_red.off()
    cross_white.off()
    print ("setting crosswalk light to " + color)
    
    if (blink==True):
        if (color=="white"):
            cross_white.blink(0.5,0.5)
        if (color=="red"):
            cross_red.blink(0.5,0.5)
    else:
        if (color=="white"):
            cross_white.on()
        if (color=="red"):
            cross_red.on()

# clear screen
#-------------------------------------------------------------
def clear_screen():
  print ("\033[2J\033[0;0f", end="")


            
# Set up lights and wait for button press
#-------------------------------------------------------------
def run_trafficlight():
    print ("")
    
    # set traffic to green and crosswalk to red
    set_trafficlight("green",False)
    set_crosswalklight("red",False)
    
    try:
        # start forever loop
        while True:
            print ("")

            # wait for button press
            print ("waiting for button press")
            button.wait_for_press()

            print ("button pressed")     
            # set traffic light to green and blinking for 4 seconds
            set_trafficlight("green",True)
            time.sleep(4)
            # set traffic light to yellow, not blinking
            set_trafficlight("yellow",False)
            time.sleep(2)

            # set traffic light to red, not blinking
            set_trafficlight("red",False)
            time.sleep(0.5)

            # set crosswalk light to white, not blinking
            set_crosswalklight("white",False)
        
            # count down - loop from 9 to 0 and show on display
            for char in '9876543210': 
                display.value = char
                print ("showing " + char)

                # when countdown at 5, make crosswalk light blink
                if (char == '5'):
                    set_crosswalklight("white",True)

                # if still above 0, play a short beep
                if (char != '0'):
                    play_buzzer(0.1)
                    time.sleep(0.9)
                else:
                    # once at 0: 
                    #   set crosswalk to red, not blinking, 
                    #   play longer beep, 
                    #   set traffic light back to green
                    set_crosswalklight("red",False)
                    play_buzzer (0.5)
                    time.sleep(0.8)
                    set_trafficlight("green",False)
                    display.value = ' '
                    
    # for CTRL-C to exit program                    
    except KeyboardInterrupt:
         print (" Exiting")
         reset_all()

# ------------------------- MAIN CODE ---------------------------
reset_all()        
clear_screen()
print("Welcome to the crosswalk!")
run_trafficlight ()
print("Thank you for crossing the street safely!")


