import re
from pathlib import Path
from dotenv import load_dotenv
import os
import spacy

# Загрузка модели spaCy для русского языка
nlp = spacy.load("ru_core_news_sm")

def search_dict_by_key_part(original_dict, key_part):
    load_dotenv('.env')
    ignore = os.getenv("IGNORE")
    result_dict = {}
    key_part_to = re.sub(r"[,?!._]", " ", key_part.lower()).split(' ')
    max_len = 0
    for key in original_dict:
        count = 0
        if Path(key).is_file() and (Path(key).stem != ignore):
            file_name = Path(key).stem.lower()
            file_name = re.sub(r"[,?!._]", " ", file_name)
            for part in key_part_to:
                if check_word_part_in_text(file_name, part):
                    count += 1
                    if count > max_len:
                        max_len = count
                        result_dict = {}
                        result_dict[key] = original_dict[key]
                    elif count == max_len:
                        max_len = count
                        result_dict[key] = original_dict[key]
    return result_dict


def swapped_dict(dict):
    swapped_dict = {v: k for k, v in dict.items()}
    return swapped_dict


def check_word_part_in_text(text, part_word):
    doc = nlp(text)
    for token in doc:
        if part_word.lower() in token.text.lower():
            return True
    return False
