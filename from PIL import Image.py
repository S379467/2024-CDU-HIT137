import numpy as np
from PIL import Image
import random

n = random.randint(0,255)
print(n)
#PLACEHOLDER

with Image.open("chapter1.jpg") as original:
    original.load()
    original.convert('RGB')
    width, height = original.size
#opens the original file; changes mode to RGB and finds the image size (in pixels)

with Image.new('RGB', (width, height), (n, n, n)) as conversion:
    conversion.load()
#creates a new image where the RGB values are all n to allow addition

original_array = np.asarray(original)
conversion_array = np.asarray(conversion)
#converts into array so RGB values can be manipulated

out_array = original_array + conversion_array #adds n to all RGB values 
"""!ISSUE after 255 it cycles back to 0 value"""
out = Image.fromarray(out_array)
out.show()


r_count = 0
for x in range(0, width):
    for y in range(0, height):
        r, g, b = out.getpixel((x, y))
        r_count = r_count + r
print("r_count is", r_count)
        


#How to save file??