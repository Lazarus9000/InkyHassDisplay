import requests
import json
#from inky import InkyPHAT
from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
import os
import time
from datetime import datetime

import buttonshim

view = 0
totalViews = 2

garbageDay = 0
garbageAlarm = 0

@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a(button, pressed):
    #buttonshim.set_pixel(0x94, 0x00, 0xd3)
    global view
    print(view)
    nextView()


@buttonshim.on_press(buttonshim.BUTTON_B)
def button_b(button, pressed):
    #buttonshim.set_pixel(0x00, 0x00, 0xff)
    print("button B")

@buttonshim.on_press(buttonshim.BUTTON_C)
def button_c(button, pressed):
    #buttonshim.set_pixel(0x00, 0xff, 0x00)
    print("button C")


@buttonshim.on_press(buttonshim.BUTTON_D)
def button_d(button, pressed):
    #buttonshim.set_pixel(0xff, 0xff, 0x00)
    print("button D")


@buttonshim.on_press(buttonshim.BUTTON_E)
def button_e(button, pressed):
    #buttonshim.set_pixel(0xff, 0x00, 0x00)
    print("button E")
    drawGarbage()


#Get current path
PATH = os.path.dirname(__file__)

# Set up the display
try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")


if inky_display.resolution not in ((212, 104), (250, 122)):
    w, h = inky_display.resolution
    raise RuntimeError("This example does not support {}x{}".format(w, h))

inky_display.set_border(inky_display.WHITE)

#Support function for images
#PNGs downloaded from https://materialdesignicons.com/ (at least the ones I have used) use the alpha channel
#the function below converts alpha to a mask 
#adopted from https://github.com/pimoroni/inky/blob/master/examples/phat/calendar-phat.py
def create_mask(source):
    """Create a transparency mask."""
    mask_image = Image.new("1", source.size)
    w, h = source.size
    for x in range(w):
        for y in range(h):
            p = source.getpixel((x, y))
            #Returns a RGBA tuple, A is used
            #print(p[3])
            #if p in mask
            if p[3] > 0:
                mask_image.putpixel((x, y), 255)

    return mask_image

#Set hass url
hassurl = "http://192.168.1.208:8123"
#Read token
f = open(os.path.join(PATH, "token.txt"), "r")
token = f.read().strip()
#print(token)



#sensor.restaffald_tid
def get_sensor(sensor):
	#Get state
	API_ENDPOINT = hassurl + "/api/states/" + sensor

	# data to be sent to api 
	data = {'Authorization':"Bearer " + token, 
			'Content-Type':'application/json'} 
  
	# sending post request and saving response as response object 
	r = requests.get(url = API_ENDPOINT, headers = data)
	#print(r)
	#print(r.text)

	#Deserialize JSON
	object = json.loads(r.text);
	#print(object)
	return object["state"]
	#print(object["state"])
	

#Draw value on display
#inky_display = InkyPHAT("red")
#inky_display.set_border(inky_display.WHITE)

def drawTemp():
	print("drawing temp")
	global inky_display
	img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
	draw = ImageDraw.Draw(img)
	
	fontSize = 16
	
	font = ImageFont.truetype(FredokaOne, fontSize)
	datefont = ImageFont.truetype(FredokaOne, 8)
	
	outTemp = get_sensor("sensor.sonoff_si7021_temperature")
	print("outTemp: ")
	print(outTemp)
	x = 48
	y = 48/2-fontSize/2
	
	draw.text((x, y), outTemp, inky_display.RED, font)
	thermometer = Image.open(os.path.join(PATH, "thermometer.png"))
	thermometermask = create_mask(thermometer)
        img.paste(inky_display.BLACK, (0, 0), thermometermask)

	now = datetime.now()
	
	current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
	draw.text((50, 85), current_time, inky_display.BLACK, datefont)
	
	inky_display.set_image(img)
	inky_display.show()

def drawGarbage():
	print("drawing garbage")
	img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
	draw = ImageDraw.Draw(img)

	fontSize = 16

	font = ImageFont.truetype(FredokaOne, fontSize)
	datefont = ImageFont.truetype(FredokaOne, 8)

	Skrald = get_sensor("sensor.restaffald_tid")
	#Skrald = skraldResp["state"]

	if(Skrald = "2 dage"):
                print("Der skal hentes affald imorn!")

	if(Skrald = "I dag"):
		print("Der skal hentes affald!")

	genbrug = get_sensor("sensor.genbrug_tid")
	#genbrug = genbrugResp["state"]

	#message = Skrald
	#w, h = font.getsize(Skrald)
	#x = (inky_display.WIDTH / 2) - (w / 2)
	#y = (inky_display.HEIGHT / 2) - (h / 2)s

	x = 48
	y = 48/2-fontSize/2

	draw.text((x, y), Skrald, inky_display.RED, font)
	garbage = Image.open(os.path.join(PATH, "delete.png"))
	garbagemask = create_mask(garbage)
	img.paste(inky_display.BLACK, (0, 0), garbagemask)

	draw.text((x, y+50), genbrug, inky_display.BLACK, font)
	genbrugIcon = create_mask(Image.open(os.path.join(PATH, "recycle.png")))
	img.paste(inky_display.BLACK, (0, 50), genbrugIcon)

	now = datetime.now()

	current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
	draw.text((50, 85), current_time, inky_display.BLACK, datefont)

	inky_display.set_image(img)
	inky_display.show()
	#Success!

def nextView():
	global view
	print(view)
	view += 1
        view = view % totalViews
	print(view)
	drawView(view)

def drawView(i):
	print(i)
	if(i == 0):
		drawGarbage()
		
	if(i == 1):
		drawTemp()
	
while(True):
	print("drawing")
        drawView(view)
	time.sleep(300)
