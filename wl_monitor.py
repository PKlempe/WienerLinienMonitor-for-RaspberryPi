#!/usr/bin/python3
import sys
import getopt
import requests
import time
import threading
import atexit
import board
import busio
import digitalio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

# =========== Configure and Initialize LCD screen ===========
# Initialise I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Set LCD dimensions
# Modify this if you have a different sized Character LCD.
lcd_columns = 16
lcd_rows = 2

# Create lcd object so we can speak to our screen
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
lcd.text_direction = lcd.LEFT_TO_RIGHT

# Clear LCD screen
lcd.clear()

# Set LCD color and turn backlight on
# Modify this if you aren't using a blue & white LCD screen.
lcd.color = [100, 0, 0]
time.sleep(1)



# Global variables
rbl_index = 0				# Index for selecting a specific RBL object in the array rbl_numbers[]
rbl_amount = 1				# Amount of RBL numbers specified by the user

# A simple class for storing and group the required data returned by the Wiener Linien API.
class RBL:
	id = 0
	line = ''
	station = ''
	direction = ''
	time = -1

# The main function where all the magic happens...
def main(lcd_lock, wake_up):
	api_key = False
	api_url = 'https://www.wienerlinien.at/ogd_realtime/monitor?rbl={rbl}&sender={apikey}'
	refresh_time = 10
	cleaning = False		# Variable which indicates if the display needs to be cleared.
	global rbl_amount		# Needed to modify global copy of rbl_amount

	# Parses the specified options and their arguments.
	try:                                
		options, remainder = getopt.getopt(sys.argv[1:], "hk:t:", ["help", "key=", "time="])
	except getopt.GetoptError:   
		usage()                         
		sys.exit(2)                     
	for opt, arg in options:
		if opt in ("-h", "--help"):   
			usage()                     
			sys.exit()                                    
		elif opt in ("-k", "--key"):
			api_key = arg
		elif opt in ("-t", "--time"):
			try:
				specified_refresh_time = int(arg)
				if specified_refresh_time > 0:
					refresh_time = specified_refresh_time
			except ValueError:    
				usage()
				sys.exit(2)
	
	# Checks if an API key and at least one RBL number has been specified by the user.
	# If not, usage message will be printed on screen and the process terminated.
	rbl_amount = len(remainder)
	if api_key == False or rbl_amount < 1:    
		usage()
		sys.exit(2)

	# Create for every RBL number specified an instance of our class named "RBL"
	# and save it in an array.
	rbl_numbers = []
	for rbl_id in remainder:
		tmp_rbl = RBL()
		tmp_rbl.id = rbl_id
		rbl_numbers.append(tmp_rbl)


	# Endless loop for updating data as long as the process is alive.
	while True:
		if wake_up.is_set():
			cleaning = True
			while wake_up.is_set():
				time.sleep(1)

		rbl = rbl_numbers[rbl_index]
		url = api_url.replace('{apikey}', api_key).replace('{rbl}', rbl.id)		# Replace the placeholders in the API url with the values specified by the user.
		response = requests.get(url)
		try:
			response.raise_for_status()						# Check if HTTP response code is 200.
		except requests.exceptions.HTTPError as ex: 		# If not, throw exception and print error message.
			print(ex)

		# Convert response into JSON and extract required data which will then be saved in our RBL objects created before.
		try:
			monitor = response.json()['data']['monitors'][0]
			line = monitor['lines'][0]
			rbl.station = monitor['locationStop']['properties']['title']
			rbl.line = line['name']
			rbl.direction = line['towards']
			rbl.time = line['departures']['departure'][0]['departureTime']['countdown']
		except:
			print("Error: Something went wrong while extracting the required data. Try again...")
		if cleaning == True:
			cleaning = False
			with lcd_lock:
				lcd.clear()
		if not wake_up.is_set():
			lcd_show(rbl, lcd_lock)
		wake_up.wait(refresh_time)


# Function which runs in a background thread and checks if a button has been pressed.
def has_button_been_pressed(lcd_lock, screen_timer, wake_up):
	while True:
		if lcd.down_button:
			screen_timer = reset_timer(lcd_lock, screen_timer)
			switch_station(False, lcd_lock, wake_up)
			time.sleep(0.2)
		elif lcd.up_button:
			screen_timer = reset_timer(lcd_lock, screen_timer)
			switch_station(True, lcd_lock, wake_up)
			time.sleep(0.2)
		#elif lcd.left_button:
			# Switch driving direction
		#elif lcd.right_button:
			# Switch driving direction
		elif lcd.select_button:
			screen_timer = reset_timer(lcd_lock, screen_timer)
			lcd_power(lcd_lock)
			time.sleep(0.2)

		else:
			time.sleep(0.1)

# Function which updates the message on the lcd screen.
def lcd_show(rbl, lcd_lock):
	optimized_message = replace_umlauts(rbl.line + ' ' + rbl.station + '\n' + '{:0>2d}'.format(rbl.time) + ' ' + rbl.direction)
	# Access lcd object only when no one else is using it and release it afterwards.
	with lcd_lock:
		lcd.message = optimized_message

# Function which turns the screen and backlight on/off.
def lcd_power(lcd_lock):
	if lcd.display == True:
		# Access lcd object only when no one else is using it and release it afterwards.
		with lcd_lock:
			lcd.display = False
			lcd.color = [0, 0, 0]
	else:
		# Access lcd object only when no one else is using it and release it afterwards.
		with lcd_lock:
			lcd.color = [100, 0, 0]
			lcd.display = True

# Function which switches between the stations specified by the user.
def switch_station(op, lcd_lock, wake_up):
	wake_up.set()
	global rbl_index
	with lcd_lock:
		lcd.clear()
		lcd.message = "Switching\n   Station..."
	if op == True:
		rbl_index += 1
	else:
		rbl_index -= 1
	if rbl_index < 0:
		rbl_index = rbl_amount - 1
	elif rbl_index >= rbl_amount:
		rbl_index = 0
	wake_up.clear()

def reset_timer(lcd_lock, screen_timer):
	screen_timer.cancel()
	screen_timer = threading.Timer(20.0, lcd_power, args=[lcd_lock])
	screen_timer.start()
	return screen_timer

# Function which replaces all German umlauts.
def replace_umlauts(s):
    s = s.replace(chr(196), "Ae") # A umlaut
    s = s.replace(chr(214), "Oe") # O umlaut
    s = s.replace(chr(220), "Ue") # U umlaut
    s = s.replace(chr(228), "ae") # a umlaut
    s = s.replace(chr(246), "oe") # o umlaut
    s = s.replace(chr(252), "ue") # u umlaut
    s = s.replace(chr(223), "ss") # sharp s
    return s

# Function which prints a usage/help message for this script.
def usage():
	print('usage: ' + __file__ + ' [-h] [-t time] -k apikey rbl [rbl ...]\n')
	print('arguments:')
	print('  -k, --key=\tAPI key')
	print('  rbl\t\tRBL number\n')
	print('optional arguments:')
	print('  -h, --help\tShow this help')
	print('  -t, --time=\tRefresh time in seconds (Default: 10)')


def cleanup():
	lcd.clear()
	lcd.display = False
	lcd.color = [0, 0, 0]

# Check if script is the main program and therefore wasn't called by someone else.
# If yes, start executing main function.
if __name__ == "__main__":
	lcd_lock = threading.Lock()		# Mutex lock to ensure that only one thread at a time can have access to the display
	wake_up = threading.Event()		# Object for waking up the main thread to prevent waiting for the refresh time to run out
	screen_timer = threading.Timer(20.0, lcd_power, args=[lcd_lock])
	listener_thread = threading.Thread(target=has_button_been_pressed, args=[lcd_lock, screen_timer, wake_up])
	listener_thread.start()
	screen_timer.start()
	atexit.register(cleanup)		# Function to call when process terminates.
	main(lcd_lock, wake_up)