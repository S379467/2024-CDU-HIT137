

quit() #ACHIVE FOR WEEK2 CODE PDF PAGE 1-5


#TYPE FIND PROGRAM
def typefind(x):
    print(x, "is a type of", type(a))

a=5
typefind(a)
b=2.5
typefind(b)

set1 = {5, 2, 3, 2, 4}
print(set1) #typefind(set1) gives int... i don't know why
print((type(set1)))


#MAX AND MIN PROGRAM
first=int(input("enter first int"))
second=int(input("enter second int"))
if first>second:
    maximum=first
    minimum=second
else:
    maximum=second
    minimum=first
print("maximum:",maximum, "\nminimum:", minimum)

print("using built in function:", "\nmaximum is", max(first,second))
print("minimum is", min(first,second))


#PRINT N TIMES PROGRAM
for eachPass in range(0,12,3):
    print("it is alive", end="\n")


#EXPONENT PROGRAM
number=int(input("insert int to exponate: "))
exponent=5
product=1 #placeholder int

print("To the power up unitl", exponent)
for n in range(exponent):
    product=product*number
    print(product, end=" ")


#SUM IN A RANGE
print("adding all numbers between upper and lower bounds")
lower=int(input("lower bound: "))
upper=int(input("upper bound: "))
sum = 0

for count in range(lower, upper+1):
    sum=sum+count
    print("working count", count, "working sum", sum)
print("\nfinal sum is", sum)


#NUMBER GUESS PROGRAM
condition = True
number = 23
while condition:
    guess=int(input("Guess my number "))
    if guess==number:
        print("Yes")
        condition = False
    elif guess<number:
        print("Higher")
    else:
        print("Lower")
print("END")