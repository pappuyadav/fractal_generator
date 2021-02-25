from PIL import Image, ImageDraw, ImageFont
from collections import defaultdict
from math import floor, ceil
from math import log, log2
import matplotlib.pyplot as plt

MAX_ITER = 100  #Change this to see different shades of colors for your fractals.

def fractal(c, z0):
    z = z0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z*z + c
        n += 1

    if n == MAX_ITER:
        return MAX_ITER
    
    return n + 1 - log(log2(abs(z)))

def linear_interpolation(color1, color2, t):
    return color1 * (1 - t) + color2 * t 

WIDTH = 600
HEIGHT = 480
X_POS = WIDTH-WIDTH/2
Y_POS = HEIGHT-HEIGHT//18
RE_START = -1
RE_END = 1
IM_START = -1.2
IM_END = 1.2

font = ImageFont.load_default()
c = complex(0.285, 0.01) #Change these values to generate your own interesting fractals!

histogram = defaultdict(lambda: 0)
values = {}
for x in range(0, WIDTH):
    for y in range(0, HEIGHT):
        # Convert pixel coordinate to complex number
        z0 = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
                    IM_START + (y / HEIGHT) * (IM_END - IM_START))
        # Compute the number of iterations
        m = fractal(c, z0)
        
        values[(x, y)] = m
        if m < MAX_ITER:
            histogram[floor(m)] += 1

total = sum(histogram.values())
hues = []
h = 0
for i in range(MAX_ITER):
    h += histogram[i] / total
    hues.append(h)
hues.append(h)
 
im = Image.new('HSV', (WIDTH, HEIGHT), (0, 0, 0))
draw = ImageDraw.Draw(im)

for x in range(0, WIDTH):
    for y in range(0, HEIGHT):
        m = values[(x, y)]  
        hue = 255 - int(255 * linear_interpolation(hues[floor(m)], hues[ceil(m)], m % 1))
        saturation = 255
        value = 255 if m < MAX_ITER else 0
        # Plot the point
        draw.point([x, y], (hue, saturation, value))
        draw.text((X_POS, Y_POS), "Congratulations! This is your generated fractal!!", (0,0,255), font=font)
        
im.convert('RGB').save('your_fractal.png', 'PNG')
im.show()
