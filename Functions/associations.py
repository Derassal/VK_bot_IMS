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
    },
    'to_rus': {
        'a': 'а', 'b': 'б', 'c': 'к', 'd': 'д', 'e': 'е', 'f': 'ф', 'g': 'г',
        'h': 'х', 'i': 'и', 'j': 'й', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н',
        'o': 'о', 'p': 'п', 'q': 'к', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у',
        'v': 'в', 'w': 'в', 'x': 'кс', 'y': 'и', 'z': 'з', 'ñ': 'нь', 
        'á': 'а', 'é': 'е', 'í': 'и', 'ó': 'о', 'ú': 'у', 'ü': 'у'
    }
}

def load_w(l_t):
    files = {'rus': 'words.db', 'es': 'spanish_words.db', 'en': 'english_words.db'}
    path = f"Databases/{files.get(l_t, 'words.db')}"
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("SELECT word FROM words")
        res = list()
        for el in cur.fetchall():
            res.append(el[0])
        conn.close()
        return res
    except:
        return list()

def p_cent(a, b):
    if not b: return 0
    return math.ceil(100 - (lev(a, b) / max(len(b), 1)) * 100)

def split_s(word, lang):
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

def transf(word, l_f, l_t):
    word = word.lower()
    if l_f == l_t: 
        return word
    if l_f == 'rus' and l_t in MAPS:
        m = list()
        for ch in word: 
            m.append(MAPS[l_t].get(ch, ch))
        return "".join(m)
    if l_t == 'rus' and l_f != 'rus':
        m = list()
        for ch in word: 
            m.append(MAPS['to_rus'].get(ch, ch))
        return "".join(m)
    return word

def give(word, orig, base, l_t):
    syls = split_s(word, l_t)
    res = list()
    res.append(f"{orig} = {word}:")
    for s in syls:
        match = None
        if not base:
            match = "ошибка базы"
        else:
            for el in base:
                if el.lower().startswith(s.lower()):
                    match = el
                    break
            if not match:
                best = max(base, key=lambda x: p_cent(s, x))
                match = best if p_cent(s, best) >= 10 else "???"
        res.append(f"{s} => {match}")
    return "\n".join(res)

def get_sync(text, pair):
    l_f, l_t = pair.split()
    base = load_w(l_t)
    words = text.lower().split()
    orig = list(words)
    proc = list()
    for w in words:
        proc.append(transf(w, l_f, l_t))
    res = list()
    for i in range(len(proc)):
        res.append(give(proc[i], orig[i], base, l_t))
    return res

async def get_full_line(text, pair):
    return await asyncio.to_thread(get_sync, text, pair)