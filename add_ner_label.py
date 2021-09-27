import os
from os.path import exists, dirname

import spacy

nlp = spacy.blank("de")

ner = nlp.add_pipe("ner", name="religion_ner")
ner.add_label("REL")
save_path = "models/personal_ner"
if not exists(dirname(save_path)):
    os.makedirs(dirname(save_path))
ner.to_disk(save_path)
