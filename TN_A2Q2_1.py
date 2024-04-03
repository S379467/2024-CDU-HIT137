#pop any ideas you have in the comments, this summarises Assignment 2Q2.1

"""QUESTION TWO
Chapter 1: create a new image to change rgb of image.
Add all r pixel values in new_image and find the sum. 
    use code below to generate number to modify code"""
#Lecturer mentioned that he covered image conversion in a lecture, have you watched it?



#TEXT ON ASSIGNEMENT SHEET
import time

current_time = int(time.time())

generated_number = (current_time % 100) + 50

if generated_number % 2 == 0:
    generated_number += 10

print(generated_number)