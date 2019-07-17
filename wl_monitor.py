import sys
import getopt
import requests
import time
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

# =========== Configure and Initialize LCD screen ===========
# Modify this if you have a different sized Character LCD
lcd_columns = 16
lcd_rows = 2

# Initialise I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Initialise the LCD class
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
lcd.text_direction = lcd.LEFT_TO_RIGHT

# Clear the LCD screen
lcd.clear()

# Set LCD color
lcd.color = [255, 0, 0]
time.sleep(1)



# A simple class for storing and group the required data returned by the Wiener Linien API.
class RBL:
	id = 0
	line = ''
	station = ''
	direction = ''
	time = -1

# The main function where all the magic happens...
def main(argv):
	api_key = False
	api_url = 'https://www.wienerlinien.at/ogd_realtime/monitor?rbl={rbl}&sender={apikey}'
	refresh_time = 10

	try:                                
		opts, args = getopt.getopt(argv, "hk:t:", ["help", "key=", "time="])
	except getopt.GetoptError:   
		usage()                         
		sys.exit(2)                     
	for opt, arg in opts:
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
	if api_key == False or len(args) < 1:    
		usage()
		sys.exit(2)

	# Create for every RBL number specified an instance of our class named "RBL"
	# and save it in an array.
	rbl_numbers = []
	for rbl_id in args:
		tmp_rbl = RBL()
		tmp_rbl.id = rbl_id
		rbl_numbers.append(tmp_rbl)

	# Endless loop for updating data as long as the process is alive.
	while True:
		for rbl in rbl_numbers:
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

			lcdShow(rbl)
		time.sleep(refresh_time)


# Function which updates the message on the lcd screen.
def lcdShow(rbl):
	optimizedMessage = replaceUmlaut(rbl.line + ' ' + rbl.station + '\n' + '{:0>2d}'.format(rbl.time) + ' ' + rbl.direction)
	lcd.message = optimizedMessage

# Function which replaces all German umlauts.
def replaceUmlaut(s):
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
	print('  -h, --help\tshow this help')
	print('  -t, --time=\ttime between station updates in seconds, default 10')


# Check if script is the main program and therefore wasn't called by someone else.
# If yes, start executing main function.
if __name__ == "__main__":
	main(sys.argv[1:])