import spacy
import csv
import ast

label = {
    "дата": "Date",
    "бренд": "Brand",
    "вид спорта": "Sport",
    "видеоигра": "Game",
    "команда": "Team",
    "лига": "League",
    "локация": "Location",
    "модель": "Model",
    "название проекта": "Project name",
    "организация": "Organization",
    "персона": "Person",
    "сезон": "Season",
    "серия": "Episode"
}


f = open("ner_data_train.csv", encoding="utf-8")
f = csv.reader(f, delimiter=',')
f = list(f)
TRAINING_DATA = [] # [["sentence", {"entities": [[start_index, end_index, label], ...]}], ...]

#create training_data from dataset
for i in f[1:]:
    try:
        entities = []
        info = i[1].replace('\\', '')
        info = ast.literal_eval(info)
        k = 0
        for j in range(len(info)):
            entities.append([info[j]["offset"], info[j]["offset"] + info[j]["length"], label[info[j]["label"].lower()]])
        TRAINING_DATA.append([i[0], {"entities": entities}])
    except Exception:
        continue



from spacy.tokens import DocBin

nlp = spacy.load("ru_core_news_sm")
db = DocBin() # create a DocBin object
cnt = 0
import os
from tqdm import tqdm
for text, annot in tqdm(TRAINING_DATA): # data in previous format
    doc = nlp.make_doc(text) # create doc object from text
    ents = []
    for start, end, label in annot["entities"]: # add character indexes
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is None:
            cnt += 1
            print("Skipping entity")
        else:
            ents.append(span)
    doc.ents = ents # label the text with the ents
    db.add(doc)
os.chdir(r'//ai_spacy') #paste your path
db.to_disk("./train.spacy")