import re
# def find_matches(phrase1, phrase2):
#     words1 = re.split(r"\s+|,|\n|_", phrase1.lower())
#     words2 = re.split(r"\s+|;|,|\n|_", phrase2.lower())
#
#     matches = set(words1) & set(words2)
#
#     return matches
#
#
# phrase1 = "Программирование это_весело"
# phrase2 = "Весело программировать"
#
# result = find_matches(phrase1, phrase2)
# print("Совпадения в фразах:")
# for match in result:
#     print(match)

tes ={'/Users/a1234/PycharmProjects/pythonDiploma/venv/bin/python /Users/a1234/PycharmProjects/pythonDiploma/Бюджет 2022 подписанный.pdf ': 99}
def search_dict_by_key_part(original_dict, key_part):
    result_dict = {}
    key_part = re.split(r"\s+|,|\n|_|/", key_part.lower())

    for key in original_dict:
        key_spl = re.split(r"\s+|,|\n|_|/", key.lower())
        matches = set(key_part) & set(key_spl)
        matches = list(matches)
        if len(matches) > 0:
            result_dict[key] = original_dict[key]
        else:
            for key in original_dict:
                key_spl = re.split(r"\s+|,|\n|_|/", key.lower())
                for one_part in key_part:
                    for one_word in key_spl:
                        if one_part in one_word:
                            result_dict[key] = original_dict[key]
    return result_dict

print(search_dict_by_key_part(tes, '2022'))