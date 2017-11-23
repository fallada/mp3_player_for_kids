""" This is a copy from https://github.com/umarsear/ESP8266-Connected-MP3-Player/blob/master/mp3.py
     Thank you umarsear!
"""

from time import sleep
from machine import UART
uart=UART(0,9600)
import yx5300 as cmd



# set initial volume to mid point 
volume_level=15 

initialized=False

# do necessary initialization
# Currently only the volume is set
def initialize():
	global initialized
	global volume_level
	if not initialized:
		set_volume(volume_level)
		initialized=True
		sleep(0.4)

def next():
	initialize()		
	uart.write(cmd.play_next())

def previous():
	initialize()
	uart.write(cmd.play_previous())

def hibernate():
	uart.write(cmd.sleep_module())

def wakeup():
	uart.write(cmd.wake_module())
	
def reset():
	global initialized
	initialized=False
	uart.write(cmd.reset_module())
	
def play_track(track_id):
	initialize()
	uart.write(cmd.play_track(track_id))

def play_folder(folder_id, track_id=1):
	initialize()
	uart.write(cmd.play_folder(folder_id, track_id))

def play():
	initialize()
	play_track(1);
	
def pause():
	uart.write(cmd.pause())

def resume():
	uart.write(cmd.resume())
	
def stop():
	uart.write(cmd.stop())

def set_volume(level):
	global volume_level
	volume_level=level
	uart.write(cmd.set_volume(level))
	
def volume_up(step_count=1):
	global volume_level
	volume_level=volume_level+step_count
	set_volume(volume_level)
			
def volume_down(step_count=1):
	global volume_level
	volume_level=volume_level-step_count
	set_volume(volume_level)

def mute():
	uart.write(cmd.set_volume(0))
	
def unmute():
	global volume_level
	uart.write(cmd.set_volume(volume_level))

def get_volume():
	global volume_level
	return volume_level
