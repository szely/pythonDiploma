import re
# def search_phrases(text, phrases):
#     matched_phrases = []
#     for phrase in phrases:
#         if phrase in text:
#             matched_phrases.append(phrase)
#     return matched_phrases

def search_dict_by_key_part(original_dict, key_part):
    result_dict = {}
    key_part = re.split(r"\s+|,|\n|_|/", key_part.lower())

    for key in original_dict:
        key_spl = re.split(r"\s+|,|\n|_|/", key.lower())
        matches = set(key_part) & set(key_spl)
        matches = list(matches)
        if len(matches) > 0:
            result_dict[key] = original_dict[key]
    return result_dict

def swapped_dict(dict):
    swapped_dict = {v: k for k, v in dict.items()}
    return swapped_dict