import json
import pandas as pd
from tkinter import messagebox

def name_to_filename(name: str) -> str:
    """
    name_to_filename takes a flashcard's name as an input and outputs the appropriate file_name
    """
    filename = name.lower()
    for i in range(0, len(filename)):
        if 32 <= ord(filename[i]) <= 39 or 42 <= ord(filename[i]) <= 47 or 58 <= ord(filename[i]) <= 64:
            filename = filename.replace(filename[i], '_')
        elif 91 <= ord(filename[i]) <= 94 or 58 <= ord(filename[i]) <= 64 or ord(filename[i]) == 96:
            filename = filename.replace(filename[i], '_')
        elif 123 <= ord(filename[i]) <= 127:
            filename = filename.replace(filename[i], '_')
    return filename


def FlashCard_Created(flashcard_name: str, flashcard_color: str, flashcard_card_count: int = 0):

    collection = {
        'collection_name': flashcard_name,
        'collection_color': flashcard_color,
        'collection_card_count': flashcard_card_count,
        'day_and_words': []
    }
    supercollection = {
        'collection_name': flashcard_name,
        'collection_color': flashcard_color,
        'collection_card_count': flashcard_card_count
    }
    filename = name_to_filename(flashcard_name)
    pd.DataFrame([('Question', 'Answer')]).to_csv('data/' + filename + '.csv', header=False, index=False, mode='a')
    path = 'serialfiles/' + filename + '.json'

    with open(path, 'w') as file:
        json.dump(collection, file, indent=2)

    with open('serialfiles/SuperFile.json') as file:
        existing_data = json.load(file)
    if type(existing_data) is dict:
        existing_data = [existing_data]

    existing_data.append(supercollection)

    with open('serialfiles/SuperFile.json', 'w') as file:
        json.dump(existing_data, file, indent=2)


def Card_Count_Changer(number_of_cards: int, collection_name: str):
    if number_of_cards < 0:
        number_of_cards = 0

    with open('serialfiles/SuperFile.json') as superfile:
        existing_data = json.load(superfile)

    if type(existing_data) is dict:
        existing_data = [existing_data]

    for data in existing_data:
        if str(data["collection_name"]) == collection_name:
            data["collection_card_count"] = number_of_cards
            break

    with open('serialfiles/SuperFile.json', 'w') as superfile:
        json.dump(existing_data, superfile, indent=2)

    path = 'serialfiles/' + name_to_filename(collection_name) + '.json'

    with open(path, 'r') as file:
        file_data = json.load(file)

    file_data["collection_card_count"] = number_of_cards

    with open(path, 'w') as file:
        json.dump(file_data, file, indent=2)


def read_from_csv(collection_name: str):
    path = 'data/' + name_to_filename(collection_name) + '.csv'
    try:
        reader = pd.read_csv(path)
    except FileNotFoundError:
        messagebox.showerror("ERROR", "NO DATA HAS BEEN FOUND!")
    else:
        data = reader.to_dict(orient='records')
        return data
