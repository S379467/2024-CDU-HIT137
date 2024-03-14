

quit() #ARCHIVE FOR WEEK2 PDF PAGES 6-8


#ADD USER INPUT PROGRAM
sum=0.0
data=input("enter float or nothing to quit ")
while data != "":
    num=float(data)
    sum=sum+num
    data=input("enter float or nothing to quit ")
print("the sum is", sum)


#RANGE FIND PROGRAM
while True:
    number=int(input("Enter int ot find range, enter to kill program "))
    if number >=30 and number <=90:
        break
    else:
        print("NOT IN RANGE TRY AGAIN")
print("Good job", number, "is within the range")


#RANDOM FIBONACCI PROGRAM
a,b = 0,1
while b<10:
    print(b, end=" ")
    a, b = b, a+b


#RANDOM NUMBER PROGRAM
import random #i think this uses a randos python def/module
for roll in range(10):
    print(random.randint(1,6), end=" ")


#COUNTRY COUNT PROGRAM
country = ['Australia', 'America', 'Austria']
for c in country:
    print (c, len(c))