

quit() #ARCHIVE FOR WEEK3


#ARRAY OPERATION PROGRAM
a=[1,3,5,7,9]
sum=0
for i in range(5):
    sum=sum+a[i]
print(sum)

b=[]
sum=0
for i in range(5):
    x=int(input("Enter integer no: "))
    b.append(x)
print(b)
for i in range(5):
    sum=sum+b[i]
print('sum is ', sum)


#ENCRYPT DECRYPT PROGRAM
text=input("enter text to encrypt ")
dis,code=5,""
for ch in text:
    ordvalue=ord(ch)
    ciphervalue=ordvalue+dis
    if ciphervalue>ord('z'):
        x=ciphervalue-ord('z')
        ciphervalue=ord('a')+x-1
    code=code+chr(ciphervalue)
print("encrypted text is ", code )

decrypt=input("enter text to decrypt: ")
dis,code=5,""
for ch in decrypt:
    ordvalue=ord(ch)
    ciphervalue=ordvalue-dis
    if ciphervalue>ord('a'):
        x=ord('a')-ciphervalue
        ciphervalue=ord('z')-x+1
    code=code+chr(ciphervalue)
print("decryted text is: ", code)


#SENTANCE SPLITTER PROGRAM
sentance=input("enter a sentance: ")
wordlist=sentance.split()
print(wordlist)
print("there are", len(wordlist), "words")


#STRING METHOD PROGRAM
s= "Hello There :P"
print(s)
print(len(s))
print(s.center(20))
print(s.count('e'))
print(s.endswith(":P"))
print(s.isalpha())
print(s.lower())
print(s.upper())
print(s.replace('e','3'))
print(s.split(" "))
print(s.split(" ")[-1])


#FILE TXT CREATION AND READING PROGRAM
f = open("myfirst.txt", 'w')
f.write("First line \nSecond line. \n")
f.close()

f = open("myfirst.txt", 'r')
text=f.read()
print(text)


#RANDOM NUMBER AND SUM TXT PROGRAM
import random
f=open("integers.txt", 'w')
for count in range(500):
    number=random.randint(1,500)
    f.write(str(number)+"\n")
f.close()

f=open("integers.txt", 'r')
sum=0
for line in f:
    wordlist=line.split()
    for word in wordlist:
        number=int(word)
        sum=sum+number
print(sum)
f.close()