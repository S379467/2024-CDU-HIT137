
"""PART 1: This program takes two user inputs and divides them into the corresponding class (int, str or tuple) and applys different 
variants of a function to produce an output"""
#TESSA SURENDONK [S379467]


from tkinter import *
root = Tk()                     #setup the tkinter window
root.minsize(200,300)
root.maxsize(200,300)
root.configure(bg="gray")


class User_str(object):         #parent class creation
    def __init__(self,x):
        self.__x = str(x)       #dunder (encapsulation) makes sure these attributes are private and cannot be called upon outside classes
        self.__subtract = self.__x
    
    def plus(self, other):                      #inital setup of plus(), will be modified in child classes
        if isinstance(other, User_tuple):
            return other.plus(self)             #calls upon child class User_tuple to consoilidate code
        return User_str(self.__x + other.__x)   #result is a User_str so we can later call upon self.value (decorator)
    
    def subtract(self, other):
        other_subtract = "-"
        for i in other.__x:
            if i in self.__subtract:
                self.__subtract = self.__subtract.replace(i, "", 1)
            else: other_subtract = other_subtract+i
        return User_str(f"{self.__subtract}{other_subtract}")

    def multiply(self, other):
        if isinstance(other, User_tuple):
            return other.multiply(self)
        result = ""
        for i in self.value:
            for j in other.value:
                result = result + i + j
        return User_str(result)

    @property               #(decorator) property is used so the method is treated like a member feild, will not take inputs.                     
    def value(self):        #@value.setter is not used so self.value remains immutable
        return self.__x
 
    
class User_int(User_str):           #(inheritance) this child class takes all methods from the parent class
    def __init__(self, x):
        if not isinstance(x, int):
            raise Exception("Must be an int")
        self.__x = int(x)
        super().__init__(x)         #(inheritance) child class takes __init__ from parent

    def plus(self, other):                      #(method overwriting) redefining what the .plus() method does for User_int
        if not isinstance(other, User_int):     #(polymorphism) the .plus() method can be used on a variety of different classes
            if isinstance(other, User_tuple):
                return other.plus(self)         #refers isinstance to User_tuples.plus()
            return super().plus(other)          #calls upon parents definition of the .plus() method
        return User_int(self.__x + other.__x)

    def subtract(self, other):
        if not isinstance(other, User_int):
            return super().subtract(other)            
        return User_int(self.__x - other.__x)
    
    def multiply(self, other):
        if not isinstance(other, User_int):
            if isinstance(other, User_tuple):
                return other.multiply(self)
            return super().multiply(other)
        return User_int(self.__x * other.__x)  

    @property               #(decorator), int_value is seperate to parent self.value
    def int_value(self):
        return self.__x


class User_tuple(User_str):
    def __init__(self, x, y):
        super().__init__(f'({x.value},{y.value})')          #(polymorphism) if parent methods are used treat self as a string
        self.__x = x
        self.__y = y

    def plus(self, other):                                  #(method overiding) redefining .plus() again for User_tuple
        if not isinstance(other, User_tuple):
            return User_tuple(self.__x.plus(other), self.__y)                
        return User_tuple(self.__x.plus(other.__x), self.__y.plus(other.__y))
    
    def subtract(self, other):
        if not isinstance(other, User_tuple):
            return User_tuple(self.__x.subtract(other), self.__y)
        return User_tuple(self.__x.subtract(other.__x), self.__y.subtract(other.__y))

    def multiply(self, other):
        if not isinstance(other, User_tuple):
            return User_tuple(self.__x.multiply(other), self.__y)
        return User_tuple(self.__x.multiply(other.__x), self.__y.subtract(other.__y))

    @property
    def tuple_value(self):
        return self.__x    



def class_check(x):                 #seperates textbox input into relevant classes
    if len(x.split(",")) == 2:      #checks for tuple comma seperation and removes brackets
        x = x.replace("(", "").replace(")", "").replace(" ", "")
        insert_list = x.split(",")
        return User_tuple(class_check(insert_list[0]), class_check(insert_list[1]))     #create new User_tuple
    try:
        return User_int(int(x))     #tests for if input can be read as an int()
    except:
        return User_str(x)          #if all fails proccess as a str()

def printREAD():            #reads input in tkinter textbox
    x = class_check(entry_1.get())
    y = class_check(entry_2.get())
    return (x, y)



def button_plus():
    global calculate            
    x, y = printREAD()                      #seperates into classes
    answer = x.plus(y).value                #(polymorphism) changes what .plus() does according to class type
    calculate.configure(text=answer)        #modifys text in result tkinter display

def button_subtract():
    global calculate
    x, y = printREAD()
    answer = x.subtract(y).value            #(inheritance) .value will always produce a str() due to parents definition
    calculate.configure(text=answer)

def button_multiply():
    global calculate
    x, y = printREAD()
    answer = x.multiply(y).value
    calculate.configure(text=answer)



#creating the tkinter user interface, buttons and text
title = Label(root, text="CALCULATOR PROGRAM", bg="gray", font="TkDefaultFont 11 bold")
title.pack()
subheading = Label(root, text="insert an int, str or tuple (x,y)", bg="gray")
subheading.pack()


entry_1 = Entry(root)
entry_1.pack(pady=10)

place_holder = Label(root,bg="gray")
place_holder.pack(pady=4)

button_1 = Button(root, text="ADD", command=button_plus)            #buttons call on class methods
button_1.place(x=50, y=90)
button_2 = Button(root, text="SUBTRACT", command=button_subtract)
button_2.place(x=87, y=90)
button_3 = Button(root, text="MULTIPLY", command=button_multiply)
button_3.pack(pady=5)

entry_2 = Entry(root)
entry_2.pack(pady=10)


result = Label(root, text="RESULT", bg="gray", font="TkDefaultFont 10 bold")
result.pack(pady=10)

calculate = Label(root, text="", font="TkDefaultFont 10")
calculate.pack(fill=X, ipady=10)            #calculate text is modified in accordance to the answer

root.mainloop()