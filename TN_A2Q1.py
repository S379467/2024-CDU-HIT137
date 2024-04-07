#pop any ideas you have in the comments, this summarises Assignment 2Q1

"""QUESTION ONE
Task 1: extract csv files into a single .txt file"""

import pandas as pd

def combineCSV():
    for i in range(1,5):
        if i == 1:
            text = pd.read_csv(f"CSV{i}.csv")['SHORT-TEXT']
            with open("master.txt", 'w') as master:
                master.write("\n".join(text))
        else:
            text = pd.read_csv(f"CSV{i}.csv")['TEXT']
            with open("master.txt", 'a') as master:
                master.write("\n")
                master.write("\n".join(text))

#to activate def un-comment code below:

#combineCSV():


"""Task 2: Install 
    SpaCy – scispaCy – ‘en_core_sci_sm’/’en_ner_bc5cdr_md’).
    Transformers (Hugging Face)
    (BioBert)"""
#https://allenai.github.io/scispacy/
#https://huggingface.co/docs/transformers/en/installation

#use venv pip install




"""Task 3:
    3.1: Count words and find top 30 most common, store in csv file
    #the only way I can think to do this using pythons inbuilt system is to itterate through every word and create a list and/or count of the frequency
     but the file is so large this seems impractical
    
    3.2: Use Auto Tokenizer to make a function to count unique tokens in top 30 words"""
#3.1 seperate each word in txt. and loop that itterates through it and counts frequency? 
#Any other ideas how to go about it?
#i don't know how the auto tokenizer will work given that the highest frequency words will be joining words and the headinds of each seciton within TEXT




"""Task 4: Extract 'drug' and 'diseases' entites in txt. file, compare difference between two models"""
#No clue yet...
