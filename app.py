# -*- coding: utf-8 -*-
import json
import re
from typing import Dict, List
from collections import Counter

# Получение данных с твитами
with open('tweets.json') as json_file:
    tweets_data = json.load(json_file)

# Колличество хэштегов и слов наиболее часто встречающихся популярных хэштегов
top_count_tag = 10
top_count_words = 5

# Регулярные выражения
re_tags = re.compile('#.+')
re_words = re.compile('^[a-zA-Zа-яА-Я]*$')


# Утилиты
def _search_top_tags_words(
        regexp: re.Pattern,
        tweets: List[str],
        count_top: int,
        match: re.Pattern = None
        ) -> List[str]:
    # """Поиск часто встречающихся хэштегов, слов c условием Args(count_top).
    # Args:
    #     regexp (re.Pattern): регулярное выражение
    #     tweets (List[str]): данные с постами
    #     count_top (int): колличество хэштегов или слов для хэштегов
    #     match (re.Pattern): регулярное выражение
    # Returns:
    #     List[str]: Словарь c наиболее часто встречающиемся хэштегов, слов.
    # """
    # Фильтрация данных с твитами
    filter_list = filter(regexp.findall, tweets)
    # Конвертация строк разделенными через пробел в список
    converted_list = ' '.join(filter_list).lower().split()
    # Дополнительная фильтрация данных для слов
    if match is not None:
        converted_list = [i for i in converted_list if match.match(i)]
    # Cортировка по убыванию относительно колличества хэштегов и слов
    sorted_top = Counter(converted_list)
    # Формитирование топа по ключам
    formatted_top = [key for key, _ in sorted_top.most_common(count_top)]
    return formatted_top


def _converted_data(tweets: List[str]) -> List[str]:
    # """Конвертация строк разделенными через пробел в список .
    # Args:
    #     regexp (re.Pattern): регулярное выражение
    #     tweets (List[str]): данные с постами
    #     top (int): колличество хэштегов или слов для хэштегов
    #     match (re.Pattern): регулярное выражение
    # Returns:
    #     List[str]: Словарь c объедененными строк.
    # """
    # Объединение списка строк c твитами
    return ' '.join(tweets).split()


# Топ 10 популярных хэштегов
def _top_tags(tweets: List[str], count_tag: int = 10) -> List[str]:
    # """Возвращает словарь, наиболее часто встречающихся хэштегов.
    # Args:
    #     tweets (List[str]): данные с твитами
    #     top (int): колличество хэштегов
    # Returns:
    #     List[str]: Словарь наиболее часто встречающихся хэштегов.
    # """
    return _search_top_tags_words(re_tags, _converted_data(tweets), count_tag)


get_top_tags = _top_tags(tweets_data, top_count_tag)


# Топ 5 слов хэштега из топ 10
def _top_words(
        tweets: List[str],
        top_tags: List[str],
        count_word: int = 5
        ) -> Dict[str, List[str]]:
    # """
    # Возвращает словарь, key хэштег, value популярные слова в твитах.
    # Args:
    #     tweets (List[str]): данные с твитами
    #     top_tags (List[str]): топ хэштегов
    #     count_word (int): колличество слов
    # Returns:
    #     Dict[str, List[str]]: key хэштег,value популярные слова в твитах.
    # """
    words_by_hashtag = []
    # Поиск топ слов по популярным хэштегам без учета регистра
    for tag in top_tags:
        re_tag = re.compile(tag, re.IGNORECASE)
        # Формирование найденых слов в словарь
        list_words_by_hashtag = {
            tag:
                _search_top_tags_words(re_tag, tweets, count_word, re_words)
        }
        words_by_hashtag.append(list_words_by_hashtag)
    return words_by_hashtag


print(
    'Топ', top_count_tag, 'хэштегов:', get_top_tags,
    '\nТоп', top_count_words, 'слов для хэштегов:',
    _top_words(tweets_data, get_top_tags, top_count_words)
)
