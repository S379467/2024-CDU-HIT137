#pop any ideas you have in the comments, this summarises Assignment 2Q3

"""QUESTION THREE
Fix the encrypted error prone code. Explain fixes using comments #
"""
#the def below was used to encrypt the code we have to write a program to reverse it
def encrypt(text, key):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + key
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            encrypted_text =+ chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

#key = ????
#encrypted_code = encrypt(original_code, key)
#print(encrypted_code)

#NEXT CODE?
total = 0
for i in range(5):
    for j in range(3):
        if i + j == 5:
            total += i +j
        else:
            total -= i - j

counter = 0
while counter < 5:
    if total <13:
        total += 1
    elif total > 13:
        total -= 1
    else:
        counter += 2

#What aspect is the key?


#encrypted code to fix:

"""

tybony_inevnoyr = 100
zl_qvpg = {'xrl1':'inyhr1', 'xrl2':'inyhr2', 'xrl3':'inyhr3'}

qrs cebprff_ahzoref():
    tybony tybony_inevnoyr
    ybpny_inevnoyr = 5
    ahzoref = [1, 2, 3, 4, 5]

    juvyr ybpny_inevnoyr > 0:
        vs ybpny_inevnoyr % 2 == 0:
            ahzoref.erzbir(ybpny_inevnoyr)
        ybpny_inevnoyr -= 1
    
        erghea ahzoref

zl_frg = {1, 2, 3, 4, 5, 5, 4, 3, 2, 1}
erfhyg = cebprff_ahzoref(ahzoref=zl_frg)

qrs zbqvsl_qvpg():
    ybpny_inevnoyr = 10
    zl_qvpg['xrl4'] = ybpny_inevnoyr

zbqvsl_qvpg(5)

qrs hcqngr_tybony():
    tybony tybony_inevnoyr
    tybont_inevnoyr += 10

sbe v va enatr(5):
    cevag(v)
    v += 1

vs zl_frg vf abg Abar naq zl_qvpg['xrl4'] == 10:
    cevag("Pbaqvgvba zrg!")

vs 5 abg va zl_qvpg:
    cevag("5 abg sbhaq va gur qvpgvbanel!")

cevag(tybony_inevnoyr)
cevag(zl_qvpg)
cevag(zl_frg)

"""




