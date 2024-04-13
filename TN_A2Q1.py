import pandas as pd
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")

def combineCSV():
    for i in range(1,5):
        if i == 1:
            #CSV1 is the only file with column title 'SHORT-TEXT'
            text = pd.read_csv(f"CSV{i}.csv")['SHORT-TEXT']
            with open("master.txt", 'w') as master:
                master.write("\n".join(text))
        else:
            text = pd.read_csv(f"CSV{i}.csv")['TEXT']
            with open("master.txt", 'a') as master:
                master.write("\n")
                master.write("\n".join(text))

def simple_word_counter():
    global counter
    counter = dict()
    with open("master.txt", 'r') as master:
        for line in master:
            for word in line.split():
                word = word.lower()
                if word in counter:
                    counter[word] += 1
                else:
                    counter[word] = 1
    return counter
def biobert_word_counter():
    global tokens
    tokens = dict()
    test = open("master.txt", 'r')
    for line in test:
        token_beta = tokenizer.tokenize(line)
        for word in token_beta:             #attempt to remove subwords and non alpha characters
            if word.isalpha() == False:
                continue
            elif word in tokens:
                tokens[word] += 1
            else:
                tokens[word] = 1
    return tokens

def sort_to_csv(dict, filename):
    ordered = sorted(dict.items(), key=lambda x:x[1], reverse=True) #sets it as tuples
    highest_30 = ordered[:30]

    with open(f"{filename}.csv", 'w') as Top_30:
        for w, c in highest_30:
            Top_30.write(f"{w},{c}\n")
    

combineCSV()
sort_to_csv(simple_word_counter(), "simple_top30")
sort_to_csv(biobert_word_counter(), "biobert_top30")


"""Task 4: Extract 'drug' and 'diseases' entites in txt. file, compare difference between two models"""
#No clue yet...
