#pop any ideas you have in the comments, this summarises Assignment 2Q1

"""QUESTION ONE
Task 1: extract csv files into a single .txt file"""
#use f=open(filename, r) and f=open(filename2,w) to combine documents?

#im having issues combining the files when we use the following
"""
import pandas as pd

df = pd.read_csv("CSV4.csv")
text4 = df['TEXT'].to_list
print(text4)
"""
#it creates a series that I don't know how to convert to a txt file.
#in addition the files are still to large that the processing time is pretty long
#It seems like there is way too much text to process...


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
