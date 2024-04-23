import os
import csv
import torch
from collections import Counter
import pandas as pd
from transformers import AutoModel, AutoTokenizer
import spacy
import scispacy
import re

def combineCSV():
    for i in range(1,5):
        if i == 1:
            text = pd.read_csv(f"CSV{i}.csv")['SHORT-TEXT']
            clean_text = ' '.join(re.findall(r'\b[a-zA-Z]{4,}\b', ' '.join(text)))
            with open("master.txt", 'w') as master:
                master.write(clean_text)
        else:
            text = pd.read_csv(f"CSV{i}.csv")['TEXT']
            clean_text = ' '.join(re.findall(r'\b[a-zA-Z]{4,}\b', ' '.join(text)))
            with open("master.txt", 'a') as master:
                master.write(f"\n {clean_text}")               
def read_chunks(file, window_size=512, overlap=100):
    with open(f"{file}.txt", 'r') as f:
        long_text = f.read()
        for i in range(0, len(long_text), window_size - overlap):
            chunk = long_text[i:i + window_size]
            yield chunk

#combineCSV()       #creates file "master.txt"

def sort_to_csv(dict, result_filename, Top=30):
    ordered = sorted(dict.items(), key=lambda x:x[1], reverse=True) #sets it as tuples
    highest_30 = ordered[:Top]

    with open(f"{result_filename}.csv", 'w') as Top_30:
        for w, c in highest_30:
            Top_30.write(f"{w},{c}\n")
def simple_word_counter(file, result_filename):
    counter = dict()
    for chunk in read_chunks(file):
        word_list = chunk.split()
        for word in word_list:
            word = word.lower()
            if word in counter:
                counter[word] += 1
            else:
                counter[word] = 1
    sort_to_csv(counter, result_filename)
def biobert_word_counter(file, result_filename, model="dmis-lab/biobert-v1.1"):
    tokenizer = AutoTokenizer.from_pretrained(model)
    global unique_tokens
    unique_tokens = Counter()
    for chunk in read_chunks(file):
        tokens = tokenizer.tokenize(chunk)
        unique_tokens.update(tokens)
    sort_to_csv(unique_tokens, result_filename)

#simple_word_counter("master", "top30_simple")
#biobert_word_counter("master", "top30_simple")

def spacy_entites(model, result_filename):
    nlp = spacy.load(f"{model}")
    all_entities_spacy = []
    for chunk in read_chunks('master.txt', window_size=100000, overlap=20000):
        doc_spacy = nlp(chunk)
        entities_spacy = [(ent.text, ent.label_) for ent in doc_spacy.ents]
        all_entities_spacy.extend(entities_spacy)

    with open(f"{result_filename}.csv", 'w') as spacy_file:
        spacy_file.write('Entity,Label\n')
        for entity in all_entities_spacy:
            spacy_file.write(f'{entity[0]},{entity[1]}\n')
def biobert_entites(file, result_filename, model="dmis-lab/biobert-v1.1"):
    tokenizer = AutoTokenizer.from_pretrained(model)
    model = AutoModel.from_pretrained(model)
    all_entities_biobert = []
    for chunk in read_chunks(file):
        tokens = tokenizer.tokenize(chunk)
        input_ids = tokenizer.convert_tokens_to_ids(tokens)
        input_ids = torch.tensor([input_ids])
        outputs = model(input_ids)

        last_hidden_states = outputs.last_hidden_state
        predictions = last_hidden_states.argmax(dim=-1)
        all_entities_biobert.extend([(token, 'DISEASE') for token, label_id in zip(tokens, predictions[0])])

    with open(f"{result_filename}.csv", 'w') as biobert_file:
        biobert_file.write('Entity,Label\n')
        for entity in all_entities_biobert:
            biobert_file.write(f'{entity[0]},{entity[1]}\n')

#spacy_entites("en_core_sci_sm-0.5.3", "entities_sci")
#spacy_entites("en_ner_bc5cdr_md-0.5.3", "entities_bc5")
#biobert_entites("master", "entities_biobert")

def total_entities(file, model):
    entity_df = pd.read_csv(file)
    total = len(entity_df)
    print(f"Total Entities ({model}): {total}")
def get_most_common_words(text, Top=100):
    words = text.split()
    count = Counter(words)
    return dict(count.most_common(Top))
def compare_most_common_words(model_words, other_model_words, model_name, other_model_name):
    common_words = set(model_words) & set(other_model_words)
    unique_model_words = set(model_words) - set(other_model_words)
    unique_other_model_words = set(other_model_words) - set(model_words)
    
    max_length = max(len(common_words), len(unique_model_words), len(unique_other_model_words))
    common_words = list(common_words)[:max_length]+['']*(max_length - len(unique_other_model_words))
    unique_other_model_words = list(unique_other_model_words)[:max_length]+['']*(max_length - len(unique_other_model_words))

    total_entities_model = [len(model_words)] * max_length
    total_entities_other_model = [len(other_model_words)] * max_length

    comparison_result = {
        f"{model_name} Unique Words": unique_model_words,
        f"{other_model_name} Unique Words": unique_model_words,
        "Common Words": common_words,
        f"Total {model_name} Entities": total_entities_model,
        f"Total {other_model_name} Entities": total_entities_other_model}
    return pd.DataFrame(comparison_result, columns=[f'{model_name} Unique Words', f'{other_model_name} Unique Words', 'Common Words'])
def compare_setup(file):
    entities_to_compare = pd.read_csv(f"{file}.csv")
    return get_most_common_words(' '.join(entities_to_compare['Entity']))

"""
common_sci = compare_setup("entities_sci")
common_bc5 = compare_setup("entities_bc5")
common_biobert = compare_setup("entities_biobert")

comparison_sci_bc5cdr = compare_most_common_words(common_sci, common_bc5, 'spaCy (Sci)', 'spaCy (BC5CDR)')
comparison_sci_biobert = compare_most_common_words(common_sci, common_biobert, 'spaCy (Sci)', 'BioBERT')
comparison_bc5cdr_biobert = compare_most_common_words(common_bc5, common_biobert, 'spaCy (BC5CDR)', 'BioBERT')

comparison_sci_bc5cdr.to_csv('comparison_sci_bc5cdr.csv', index=False)
comparison_sci_biobert.to_csv('comparison_sci_biobert.csv', index=False)
comparison_bc5cdr_biobert.to_csv('comparison_bc5cdr_biobert.csv', index=False)

"""
