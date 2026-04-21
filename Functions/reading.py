import random
from Databases.words import read_db2
from state_manager import register_next_step

async def reversed_reading(message):
    await message.answer("После прочтения напишите что-нибудь, чтобы получить ответ!")
    text = random.choice(list(read_db2()))[1]
    text = str(text)
    output = []
    
    for word in text.split():
        addition = ""
        if word[-1] in ",.?!":
            addition = word[-1]
            word = word[:-1]
        output.append(word[::-1] + addition)
        
    await message.answer(" ".join(output))
    
    async def next_step(msg):
        await msg.answer(f"Текст: {text}")
        
    register_next_step(message.from_id, next_step)


async def without_vowel(message):
    await message.answer("После прочтения напишите что-нибудь, чтобы получить ответ!")
    text = random.choice(list(read_db2()))[1]
    text = str(text)
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
    text = random.choice(list(read_db2()))[1]
    text = str(text)
    output = ""
    
    for letter in text:
        if letter.lower() not in " !.,?-–":
            if random.choice([1, 0]) or letter not in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя":
                output += letter
            else:
                output += str(1 + "абвгдеёжзийклмнопрстуфхцчшщъыьэюя".index(letter.lower())) + ";"
        else:
            output += letter
            
    await message.answer(output)
    
    async def next_step(msg):
        await msg.answer(f"Текст: {text}")
        
    register_next_step(message.from_id, next_step)