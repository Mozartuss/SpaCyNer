import os
import re
import warnings
from os.path import exists, dirname

import spacy
from spacy.tokens import DocBin
from tqdm import tqdm


def load_text(file_path):
    """
    Load a text file with utf-8 encoding
    :param file_path: path to the text file
    :return: list of strings
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.readlines()
    return data


def find_entities(text):
    """
    Find the religions entries in the text sequences.
    Get the start and the end position of the words.
    Save this as entities with the entity label.
    :param text: The text sequence to view.
    :return: List with the text and the entities in a dict
    """
    religions = load_text("data/Religionen.txt")
    entities = []
    for religion in religions:
        religion = religion.strip()
        if religion in text:
            entities = [(rel.start(), rel.end(), religion) for rel
                        in re.finditer(religion, text)]
    if len(entities) > 0:
        return [text, {"entities": entities}]
    return None


def transform_to_spacy(TRAIN_DATA, save_path):
    nlp = spacy.blank("de")
    db = DocBin()
    try:
        for text, annotation in tqdm(TRAIN_DATA):
            doc = nlp.make_doc(text)
            entities = []
            for start, end, label in annotation["entities"]:
                span = doc.char_span(start, end, label=label,
                                     alignment_mode="contract")
                if span is None:
                    msg = f"Skipping entity [{start}, {end}, {label}] in the following text because the character span '{doc.text[start:end]}' does not align with token boundaries:\n\n{repr(text)}\n"
                    warnings.warn(msg)
                else:
                    entities.append(span)
            doc.ents = entities
            db.add(doc)

        if not exists(dirname(save_path)):
            os.makedirs(dirname(save_path))

        db.to_disk(save_path)

        return True
    except:
        return False


if __name__ == '__main__':
    TRAIN_DATA = []
    with open("data/Religionen_Liste.txt", "r",
              encoding="utf-8") as religion_text:
        religion_list = religion_text.read().split("\n\n")
    for line in tqdm(religion_list):
        line = line.strip().replace("\n", " ")
        results = find_entities(line)
        if results is not None:
            TRAIN_DATA.append(results)

    save_path = "train_data/religion_training_data.spacy"

    if transform_to_spacy(TRAIN_DATA, save_path):
        print("Create train dataset ✅")
