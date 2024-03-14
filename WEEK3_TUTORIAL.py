

quit() #WEEK THREE TUTORIAL ARCHIVE


#QUESTION ONE [sum even and odd user input]
even, odd, condition = 0, 0, True
while condition:
    num=input("Enter a number: ")
    if num == "":
        condition=False
    else:
        num=int(num)
        if num%2 == 1:
            odd=odd+num
        else:
            even=even+num
print("Sum of even numbers:", even)
print("Sum of odd numbers:", odd)


#QUESTION TWO [make lowercase and number of vowels]
vowels={'a','e','i','o','u'}
count=0
s=str(input("Enter string: "))
s=s.lower()
for chr in s:
    if chr in vowels:
        count=count+1
    else:
        continue
print("your string", s, "has", count, "vowels")


#QUESTION THREE [Check if input is prime]
num=int(input("Enter a number: "))
if num<=2:
    print(num, "breaks my program")
for n in range(2,num):
    if num%n == 0:
        print(num, "is not a prime number")
        break
    elif n+1 == num:
        print(num, "is a prime number") 


#QUESTION FOUR [PRINT DESIRED OUTPUT]
list1=[] #this is not the intended format
for n in range(1,6):
    list1.append(n)
    print(list1) #i dont know how to do it...
#ALTERNATE
list1=[] #this is not the intended format
for n in range(1,6):
    for i in range(1, n + 1):
        print(i, end=" ")
    print(end="\n")


#QUESTION FIVE [no. of int and chr]
numbersum,lettersum =0,0
sentance=str(input("Enter a sentance: "))
for n in sentance:
    try: 
        num=int(n)
        numbersum=numbersum+1
    except:
        if n.isalpha():
            lettersum=lettersum+1
print("LETTER", lettersum)
print("NUMBER", numbersum)
