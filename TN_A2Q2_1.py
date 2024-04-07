import numpy as np
from PIL import Image
import time

current_time = int(time.time())
generated_number = (current_time % 100) + 50
if generated_number % 2 == 0:
    generated_number += 10  
n = generated_number
print("RGB values are altered by", n)

with Image.open("chapter1.png") as original:
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

out_array = original_array + conversion_array #adds n to all RGB values, if value > 255 wrap around to 0
out = Image.fromarray(out_array)
out.show()


r_count = 0
for x in range(0, width):
    for y in range(0, height):
        r, g, b = out.getpixel((x, y))
        r_count = r_count + r
print("Sum of all R values in chapter1_out is", r_count)


out.save("chapter1_out.png")
