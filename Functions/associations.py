import math
import asyncio
import random
from Databases.words import read_db
from Levenshtein import distance as lev


def _load_words():
    return [el[1] for el in read_db()]


def per_cent(a, b):
    if not b:
        return 0
    return math.ceil(100 - (lev(a, b) / max(len(b), 1)) * 100)


def split(word):
    vowels = "аеиоуыэюя"
    parts = []
    cur = ""

    for ch in word:
        cur += ch
        if ch in vowels:
            parts.append(cur)
            cur = ""

    if cur:
        parts.append(cur)

    return parts if parts else [word]


def english_to_russian(word):
    english_map = {
        'a': 'а', 'b': 'б', 'c': 'к', 'd': 'д', 'e': 'е',
        'f': 'ф', 'g': 'г', 'h': 'х', 'i': 'и', 'j': 'дж',
        'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о',
        'p': 'п', 'q': 'к', 'r': 'р', 's': 'с', 't': 'т',
        'u': 'у', 'v': 'в', 'w': 'в', 'x': 'кс', 'y': 'й', 'z': 'з'
    }

    return ''.join(english_map.get(ch, ch) for ch in word.lower())


d = {
    'а': ['а', 'a', '@'],
    'б': ['б', 'b'],
    'в': ['в', 'b', 'v'],
    'г': ['г', 'g'],
    'д': ['д', 'd'],
    'е': ['е', 'e', 'ё'],
    'ж': ['ж'],
    'з': ['з', 'z'],
    'и': ['и', 'i'],
    'й': ['й'],
    'к': ['к', 'k'],
    'л': ['л', 'l'],
    'м': ['м', 'm'],
    'н': ['н', 'n'],
    'о': ['о', 'o'],
    'п': ['п', 'p'],
    'р': ['р', 'r'],
    'с': ['с', 'c', 's'],
    'т': ['т', 't'],
    'у': ['у', 'y', 'u', 'w'],
    'ф': ['ф', 'f'],
    'х': ['х', 'x', 'h'],
    'ц': ['ц'],
    'ч': ['ч', 'ch'],
    'ш': ['ш', 'sh'],
    'щ': ['щ', 'sch'],
    'ь': ['ь', 'b'],
    'ы': ['ы', 'bi'],
    'ъ': ['ъ'],
    'э': ['э', 'e'],
    'ю': ['ю', 'io'],
    'я': ['я', 'ya']
}


def transfer(word):
    word = word.lower()

    if word.isascii():
        return english_to_russian(word)

    res = []
    for ch in word:
        for k, v in d.items():
            if ch in v:
                res.append(k)
                break

    return ''.join(res)


def give(word, original, all_words):

    syllables = split(word)

    result = [f"{original} = {word}:"]

    for s in syllables:

        direct = None

        for el in all_words:
            if el.startswith(s):
                direct = el
                break

        if not direct:
            best = max(all_words, key=lambda x: per_cent(s, x))
            score = per_cent(s, best)

            if score >= 10:
                direct = best
            else:
                direct = "???"

        result.append(f"{s} => {direct}")

    return "\n".join(result)


def _get_full_line_sync(text):

    all_words = _load_words()

    words = text.lower().split()
    original = words.copy()

    words = [transfer(w) for w in words]

    return [
        give(words[i], original[i], all_words)
        for i in range(len(words))
    ]


async def get_full_line(text):
    return await asyncio.to_thread(_get_full_line_sync, text)