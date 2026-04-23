import random
from Databases.words import read_db2
from state_manager import register_next_step

async def reversed_reading(message):
    await message.answer("После прочтения напишите что-нибудь, чтобы получить ответ!")
    data = read_db2()
    if not data:
        return
    text = str(random.choice(data)[1])
    array = []
    symbols = ",.?!:;-–\"«»()[]"
    
    for word in text.split():
        prefix = ""
        i = 0
        while i < len(word) and word[i] in symbols:
            prefix += word[i]
            i += 1
            
        remaining = word[i:]
        
        suffix = ""
        j = len(remaining) - 1
        while j >= 0 and remaining[j] in symbols:
            suffix = remaining[j] + suffix
            j -= 1
            
        clean_word = remaining[:j+1]
        array.append(prefix + clean_word[::-1] + suffix)
        
    await message.answer(" ".join(array))
    
    async def next_step(msg):
        await msg.answer(f"Текст: {text}")
        
    register_next_step(message.from_id, next_step)

async def without_vowel(message):
    await message.answer("После прочтения напишите что-нибудь, чтобы получить ответ!")
    data = read_db2()
    if not data:
        return
    text = str(random.choice(data)[1])
    output = ""
    
    for letter in text:
        if letter.lower() not in "аеёиоуыэюя":
            output += letter

    await message.answer(output)
    
    async def next_step(msg):
        await msg.answer(f"Текст: {text}")
        
    register_next_step(message.from_id, next_step)

async def half_digits(message):
    await message.answer("После прочтения напишите что-нибудь, чтобы получить ответ!")
    data = read_db2()
    if not data:
        return
    text = str(random.choice(data)[1])
    output = ""
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    
    for letter in text:
        low_letter = letter.lower()
        if low_letter not in " !.,?…:;-–\"«»()[]":
            if random.choice([1, 0]) or low_letter not in alphabet:
                output += letter
            else:
                output += str(1 + alphabet.index(low_letter)) + ";"
        else:
            output += letter
            
    await message.answer(output)
    
    async def next_step(msg):
        await msg.answer(f"Текст: {text}")
        
    register_next_step(message.from_id, next_step)