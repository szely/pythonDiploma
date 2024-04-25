def search_dict_by_key_part(original_dict, key_part):
    result_dict = {}
    for key in original_dict:
        if key_part in key:
            result_dict[key] = original_dict[key]
    return result_dict

# Example dictionary
original_dictionary = {
    "apple": 5,
    "banana": 10,
    "orange": 7,
    "pineapple": 3,
    "grape": 8
}

# Example key part to search for
key_part_to_search = "app"

# Search for the key part in the dictionary
result_dictionary = search_dict_by_key_part(original_dictionary, key_part_to_search)

# Print the result
print("Original Dictionary:")
print(original_dictionary)
print("\nResult Dictionary:")
print(result_dictionary)
