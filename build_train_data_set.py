import json
import os
import re
from os.path import exists, dirname

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


def save_data(file_path, data):
    """
    Save a list of objects as JSON
    :param file_path: path to the file
    :param data: list of objects
    :return: None
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


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
        religion = religion.strip().lower()
        if religion in text:
            entities = [(rel.start(), rel.end(), religion) for rel
                        in re.finditer(religion, text)]
    if len(entities) > 0:
        return [text, {"entities": entities}]
    return None


if __name__ == '__main__':
    TRAIN_DATA = []
    with open("data/Religionen_Liste.txt", "r",
              encoding="utf-8") as religion_text:
        religion_list = religion_text.read().split("\n\n")
    for line in tqdm(religion_list):
        line = line.strip().replace("\n", " ").lower()
        results = find_entities(line)
        if results is not None:
            TRAIN_DATA.append(results)

    save_path = "train_data/religion_training_data.json"
    if not exists(dirname(save_path)):
        os.makedirs(dirname(save_path))
    save_data(save_path, TRAIN_DATA)
