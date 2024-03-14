list30=['april','june','september','november']
list31=['january','march','may','july','august','october','december']

month=str.lower(input("MONTH dating system: "))
if month in list30:
    print("There are 30 days in", month)
elif month in list31:
    print("There are 31 days in", month)
elif month == 'february':
    test=str.lower(input("Is it a leap year? "))
    if test == 'yes':
        print("There are 29 days in", month)
    elif test == 'no':
       print("There are 28 days in", month)
    else:
        quit()
else:
    print("ENTER a vaild date next time :|")


quit() #WEEK2 TUTORIAL ARCHIVE

#QUESTION1: FIND SMALLEST TO LARGEST FROM 3 INT
largest, smallest = None, None
for n in range(3):
    num=int(input("INT size identification system: "))
    if largest is None:
        largest, smallest= num, num
    elif num>largest:
        largest=num
    elif num<smallest:
        smallest=num
print("Largest:", largest , "Smallest:", smallest)


#QUESTION2: SUM OF 10 NUMBERS
sum=0.0
for n in range(10):
    num=float(input("FLOAT summation system: "))
    sum=num+sum
    #print("ongoing calculation", sum, num)
print("SUM of FLOAT is: ", sum)


#QUESTION3: NUMBER OF DAYS IN MONTH
list30=['april','june','september','november']
list31=['january','march','may','july','august','october','december']

month=str.lower(input("MONTH dating system: "))
if month in list30:
    print("There are 30 days in", month)
elif month in list31:
    print("There are 31 days in", month)
elif month == 'febuary':
    test=str.lower(input("Is it a leap year? "))
    if test == 'yes':
        print("There are 29 days in", month)
    elif test == 'no':
       print("There are 28 days in", month)
    else:
        quit()
else:
    print("ENTER a vaild date next time :|")