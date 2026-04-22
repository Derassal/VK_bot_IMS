import asyncio
from functools import lru_cache

import nltk
import pymorphy3
from deep_translator import GoogleTranslator
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

_morph = pymorphy3.MorphAnalyzer()
_wnl = WordNetLemmatizer()

_POS_MAP = {
    'NOUN': wn.NOUN,
    'ADJF': wn.ADJ, 'ADJS': wn.ADJ,
    'COMP': wn.ADJ,
    'VERB': wn.VERB, 'INFN': wn.VERB,
    'PRTF': wn.ADJ, 'PRTS': wn.ADJ,
    'GRND': wn.VERB,
    'ADVB': wn.ADV,
    'PRED': wn.ADV,
}

def _lemmatize_ru(word: str):
    parsed = _morph.parse(word.strip().lower())[0]
    lemma = parsed.normal_form
    pos_raw = str(parsed.tag.POS) if parsed.tag.POS else 'NOUN'
    wn_pos = _POS_MAP.get(pos_raw, wn.NOUN)
    return lemma, wn_pos

@lru_cache(maxsize=1000)
def translate_text(first_lang, second_lang, text):
    translator = GoogleTranslator(source=first_lang, target=second_lang)
    return translator.translate(text)

def _get_definition_sync(word):
    try:
        lemma_ru, wn_pos = _lemmatize_ru(word)
    except Exception:
        lemma_ru, wn_pos = word.strip().lower(), wn.NOUN

    if not lemma_ru:
        return "\n(!) Ошибка, пожалуйста, проверьте написание слова..."

    try:
        word_en = translate_text('ru', 'en', lemma_ru)
    except Exception:
        return "\n(!) Не удалось получить перевод, попробуйте позже..."

    if not word_en:
        return "\n(!) Слово не распознано, проверьте написание..."

    word_en_clean = word_en.lower().split()[0] if ' ' in word_en else word_en.lower()
    word_en_lemma = _wnl.lemmatize(word_en_clean, pos=wn_pos)

    synsets = wn.synsets(word_en_lemma, pos=wn_pos)

    if not synsets:
        synsets = wn.synsets(word_en_lemma)

    if not synsets:
        return f"\n(!) Определение для слова «{lemma_ru}» не найдено."

    top_synsets = synsets[:3]
    try:
        translated_definitions = [
            translate_text('en', 'ru', syn.definition())
            for syn in top_synsets
        ]
    except Exception:
        return "\n(!) Не удалось получить определения, попробуйте позже..."

    header = f"Слово: {lemma_ru}"
    body = '\n'.join(
        f'{i + 1}) {d.capitalize()}'
        for i, d in enumerate(translated_definitions))
    return f"\n{header}\n{body}"

async def get_definition(word):
    return await asyncio.to_thread(_get_definition_sync, word)