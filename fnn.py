def find_keys_with_phrase(dictionary, phrase):
    keys_with_phrase = []
    for key in dictionary.keys():
        words = key.split('_')  # Assuming keys are separated by underscores
        for word in words:
            if phrase in word:
                keys_with_phrase.append(key)
                break  # Break the inner loop if the phrase is found in any word
    return keys_with_phrase


# Example usage:
my_dict = {
    "apple": 1,
    "/Users/a1234/Downloads/Финансовый департамент/ОТЧЕТНОСТЬ/Отчеты/Бюджет 2022 презентация.pdf'": 2,
    "orange juice": 3,
    "pear": 4,
    "grape": 5
}

phrase = "Бюд пре"
keys = find_keys_with_phrase(my_dict, phrase)
print("Keys containing the phrase '{}':".format(phrase))
print(keys)
