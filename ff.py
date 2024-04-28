# import spacy
#
# # Загрузка модели spaCy для русского языка
# nlp = spacy.load("ru_core_news_sm")
#
# def check_part_of_word(text, part):
#     doc = nlp(text)
#     for token in doc:
#         if part in token.text:
#             return True
#     return False
#
# # text = "бюджет 2022"
# # part = "бюджет"
# #
# # if check_part_of_word(text, part):
# #     print(f"Часть слова '{part}' найдена в тексте")
# # else:
# #     print(f"Часть слова '{part}' не найдена в тексте")
#
#
import nltk
# from nltk.tokenize import word_tokenize
# import pymorphy2
#
# # Загрузка русскоязычного анализатора pymorphy2
# morph = pymorphy2.MorphAnalyzer()
#
# # Текст, в котором будем искать часть слова
# text = "Пример текста для поиска части слова в нем."
#
# # Часть слова, которую будем искать
# part_of_word = "рим"
#
# # Функция для определения наличия части слова в тексте
# def check_part_of_word(text, part_of_word):
# #     tokens = word_tokenize(text)
# #     for token in tokens:
# #         normal_form = morph.parse(token)[0].normal_form
# #         if part_of_word in normal_form:
# #             return True
# #     return False
# #
# # # Проверка наличия части слова в тексте
# # if check_part_of_word(text, part_of_word):
# #     print("Часть слова найдена в тексте.")
# # else:
# #     print("Часть слова не найдена в тексте.")
#
# import nltk
# from nltk.tokenize import word_tokenize
#
# nltk.download('punkt')  # Загрузка необходимых данных для токенизации
#
# def check_word_part(text, part):
#     tokens = word_tokenize(text.lower())  # Токенизация текста и приведение к нижнему регистру
# #     for token in tokens:
# #         if part in token:
# #             return True
# #     return False
# #
# # text = "Пример текста для проверки, содержащего часть слова 'проверка'."
# # word_part = "пример тек"  # Часть слова для поиска
# #
# # if check_word_part(text, word_part):
# #     print(f"Часть слова '{word_part}' есть в тексте.")
# # else:
# #     print(f"Части слова '{word_part}' нет в тексте.")
#
# import spacy
#
# nlp = spacy.load("ru_core_news_sm")
#
#
# def check_words_in_text(text, words):
#     doc = nlp(text)
#     found_words = set()
#
#     for token in doc:
#         if token.text.lower() in words:
#             found_words.add(token.text.lower())
#
#     return found_words
#
#
# text = "Пример текста для проверки наличия слов в нем."
# words_to_check = {"слово", "несколько", "часть", "части"}
#
# found_words = check_words_in_text(text, words_to_check)
#
# if found_words:
#     print("Следующие слова найдены в тексте:")
#     for word in found_words:
#         print(word)
# else:
#     print("Слова не найдены в тексте.")


import spacy

nlp = spacy.load("ru_core_news_sm")
#
# def check_word_in_text(text, word):
#     doc = nlp(text)
#
#     for token in doc:
#         if token.text.lower() == word.lower():
#             return True
#
#     return False
#
#
# text = "Привет, как дела?"
# word_to_check = "дел"
#
# if check_word_in_text(text, word_to_check):
#     print(f"Слово '{word_to_check}' найдено в тексте")
# else:
#     print(f"Слово '{word_to_check}' не найдено в тексте")


def check_word_part_in_text(text, part_word):
    doc = nlp(text)

    for token in doc:
        if part_word.lower() in token.text.lower():
            return True

    return False


text = "Сегодня хороший день для прогулки"
part_word_to_check = "ден"

if check_word_part_in_text(text, part_word_to_check):
    print(f"Часть слова '{part_word_to_check}' найдена в тексте")
else:
    print(f"Часть слова '{part_word_to_check}' не найдена в тексте")