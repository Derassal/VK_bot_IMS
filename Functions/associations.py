import math
import asyncio
import sqlite3
from Levenshtein import distance as lev

VOWELS = {
    'rus': "аеиоуыэюяё",
    'es': "aeiouáéíóúü",
    'en': "aeiouy"
}

MAPS = {
    'es': {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'y', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'c', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'j', 'ц': 'z', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ы': 'i',
        'ь': '', 'ъ': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    },
    'en': {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ы': 'y',
        'ь': '', 'ъ': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
}

def _load_words(lang_to):
    db_files = {'rus': 'words.db', 'es': 'spanish_words.db', 'en': 'english_words.db'}
    path = f"Databases/{db_files.get(lang_to, 'words.db')}"
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("SELECT word FROM words")
        res = [el[0] for el in cur.fetchall()]
        conn.close()
        return res
    except:
        return list()

def per_cent(a, b):
    if not b: return 0
    return math.ceil(100 - (lev(a, b) / max(len(b), 1)) * 100)

def split_syllables(word, lang):
    v = VOWELS.get(lang, VOWELS['rus'])
    parts = list()
    cur = ""
    for ch in word.lower():
        cur += ch
        if ch in v:
            parts.append(cur)
            cur = ""
    if cur: parts.append(cur)
    return parts if parts else [word]

def transfer(word, lang_from, lang_to):
    word = word.lower()
    if lang_from == 'rus' and lang_to in MAPS:
        return ''.join(MAPS[lang_to].get(ch, ch) for ch in word)
    return word

def give(word, original, all_words, lang_to):
    syllables = split_syllables(word, lang_to)
    result = [f"{original} = {word}:"]
    for s in syllables:
        direct = None
        # ИСПРАВЛЕНИЕ: Защита от пустой базы
        if not all_words:
            direct = "[Ошибка: База слов пуста или не найдена]"
        else:
            for el in all_words:
                if el.lower().startswith(s.lower()):
                    direct = el
                    break
            if not direct:
                best = max(all_words, key=lambda x: per_cent(s, x))
                direct = best if per_cent(s, best) >= 10 else "???"
        result.append(f"{s} => {direct}")
    return "\n".join(result)

def _get_full_line_sync(text, lang_pair):
    l_from, l_to = lang_pair.split()
    all_words = _load_words(l_to)
    words = text.lower().split()
    original = words.copy()
    processed = [transfer(w, l_from, l_to) for w in words]
    return [give(processed[i], original[i], all_words, l_to) for i in range(len(processed))]

async def get_full_line(text, lang_pair):
    return await asyncio.to_thread(_get_full_line_sync, text, lang_pair)