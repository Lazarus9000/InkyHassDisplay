import requests
import json
#from inky import InkyPHAT
from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
import os

import buttonshim

@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a(button, pressed):
    buttonshim.set_pixel(0x94, 0x00, 0xd3)


@buttonshim.on_press(buttonshim.BUTTON_B)
def button_b(button, pressed):
    buttonshim.set_pixel(0x00, 0x00, 0xff)


@buttonshim.on_press(buttonshim.BUTTON_C)
def button_c(button, pressed):
    buttonshim.set_pixel(0x00, 0xff, 0x00)


@buttonshim.on_press(buttonshim.BUTTON_D)
def button_d(button, pressed):
    buttonshim.set_pixel(0xff, 0xff, 0x00)


@buttonshim.on_press(buttonshim.BUTTON_E)
def button_e(button, pressed):
    buttonshim.set_pixel(0xff, 0x00, 0x00)

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


#Support function for image
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
            if p in mask:
                mask_image.putpixel((x, y), 255)

    return mask_image


#Read token
f = open("token.txt", "r")
token = f.read().strip()
print(token)

#Get state
API_ENDPOINT = "http://192.168.1.208:8123/api/states/sensor.restaffald_tid"
  
# data to be sent to api 
data = {'Authorization':"Bearer " + token, 
        'Content-Type':'application/json'} 
  
# sending post request and saving response as response object 
r = requests.get(url = API_ENDPOINT, headers = data)
print(r)
print(r.text)

#Deserialize JSON
object = json.loads(r.text);
print(object)

print(object["state"])
Skrald = object["state"]

#Draw value on display
#inky_display = InkyPHAT("red")
#inky_display.set_border(inky_display.WHITE)

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

font = ImageFont.truetype(FredokaOne, 16)

message = Skrald
w, h = font.getsize(Skrald)
x = (inky_display.WIDTH / 2) - (w / 2)
y = (inky_display.HEIGHT / 2) - (h / 2)

draw.text((x, y), message, inky_display.RED, font)
inky_display.set_image(img)
inky_display.show()

icon = Image.open(os.path.join(PATH, "delete.png"))
iconmask = create_mask(icon, [inky_display.WHITE])
img.paste(inky_display.WHITE, (10, 10), iconmask)

#Success!


