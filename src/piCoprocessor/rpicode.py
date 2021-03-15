import os, sys, digitalio, board, busio
 
from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
from adafruit_lc709203f import LC709203F
import adafruit_bmp3xx





i2c = busio.I2C(board.SCL, board.SDA)




# Create sensor objects
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
battSensor = LC709203F(i2c)





cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000
display = st7789.ST7789(board.SPI(), cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE, width=135, height=240, x_offset=53, y_offset=40)
height = disp.width
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
padding = -2
top = padding
bottom = height - padding
x = 0
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

while True:
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    ip = 'cock'
    CPU = 'and'
    Disk = 'ball'
    Temp = 'torture'
    y = top
    draw.text((x, y), IP, font=font, fill="#FFFFFF")
    y += font.getsize(IP)[1]
    draw.text((x, y), CPU, font=font, fill="#FFFF00")
    y += font.getsize(CPU)[1]
    draw.text((x, y), MemUsage, font=font, fill="#00FF00")
    y += font.getsize(MemUsage)[1]
    draw.text((x, y), Disk, font=font, fill="#0000FF")
    y += font.getsize(Disk)[1]
    draw.text((x, y), Temp, font=font, fill="#FF00FF")
 
    # Display image.
    disp.image(image, rotation)
    time.sleep(1)
