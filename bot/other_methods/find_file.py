import re
from pathlib import Path
from dotenv import load_dotenv
import os

def search_dict_by_key_part(original_dict, key_part):
    load_dotenv('.env')
    ignore = os.getenv("IGNORE")
    result_dict = {}
    key_part = re.split(r"\s+|,|\n|_|/", key_part.lower())

    max_len = 0
    for key in original_dict:
        if Path(key).is_file() and (Path(key).stem != ignore):
            key_spl = re.split(r"\s+|,|\n|_|/", key.lower())
            matches = set(key_part) & set(key_spl)
            len_matches = len(list(matches))
            if len_matches > max_len:
                max_len = len_matches
                result_dict = {}
                result_dict[key] = original_dict[key]
            if len_matches == max_len:
                result_dict[key] = original_dict[key]
            # else:
            #     for key in original_dict:
            #         if Path(key).is_file() and (Path(key).stem != ignore):
            #             key_spl = re.split(r"\s+|,|\n|_|/", key.lower())
            #             for one_part in key_part:
            #                 for one_word in key_spl:
            #                     if one_part in one_word:
            #                         result_dict[key] = original_dict[key]
    return result_dict

def swapped_dict(dict):
    swapped_dict = {v: k for k, v in dict.items()}
    return swapped_dict