import requests
import json
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
import os

#Read token
f = open("token.txt", "r")
token = f.read()
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
inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.WHITE)

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

font = ImageFont.truetype(FredokaOne, 22)

message = "Hello, World!"
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


def create_mask(source, mask=(inky_display.WHITE, inky_display.BLACK, inky_display.RED)):
    """Create a transparency mask.
    Takes a paletized source image and converts it into a mask
    permitting all the colours supported by Inky pHAT (0, 1, 2)
    or an optional list of allowed colours.
    :param mask: Optional list of Inky pHAT colours to allow.
    """
    mask_image = Image.new("1", source.size)
    w, h = source.size
    for x in range(w):
        for y in range(h):
            p = source.getpixel((x, y))
            if p in mask:
                mask_image.putpixel((x, y), 255)

    return mask_image