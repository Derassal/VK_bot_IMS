import random
import asyncio
from Databases.database import find_user_id_by_tg_id, get_user_by_id
from Databases.words import read_db
from state_manager import register_next_step

def dict_to_list(d):
    return [f"{int(key) + 1} - {value}" for key, value in d.items()]

async def check_case(message, cases, case_id, correct_answer):
    if message.text.lower() != "/конец":
        is_correct = message.text.lower() == correct_answer.lower()
        await message.answer("Удачно!" if is_correct else f"Не-не. Правильно: {correct_answer}")
        await give_case(message, cases, case_id + 1)
    else:
        await message.answer("Ну ладно :((")

async def give_case(message, cases, case_id):
    if case_id >= len(cases):
        return await message.answer("Слова закончились...")
        
    item, correct_answer = cases[case_id]
    await message.answer(f"Необходимо ответить на: {int(item) + 1}")
    
    async def next_step(msg):
        await check_case(msg, cases, case_id, correct_answer)
        
    register_next_step(message.from_id, next_step)

def make_right(list_, how_many):
    new = dict()
    for count, el in enumerate(range(1, how_many + 1)):
        new[count] = f'{random.choice(list_)}'
    return new

async def training(message):
    # Загружаем базу слов
    words_all = read_db()
    words_all = [str(el[1]) for el in words_all]
    
    # Получаем настройки пользователя
    user_data = list(get_user_by_id(find_user_id_by_tg_id(int(message.from_id))))
    
    # Настройки: user_data[5] - кол-во слов, user_data[4] - время на одно слово
    count_words = int(user_data[5])
    time_per_word = int(user_data[4])
    
    content = make_right(words_all, count_words)
    job = '\n'.join(dict_to_list(content))
    
    # Считаем общее время ожидания
    total_time = time_per_word * len(content)
    
    # Отправляем список слов и сохраняем объект сообщения
    sent_msg = await message.answer(f"{job}\n\n⏱ У тебя есть {total_time} секунд!")
    
    # Ждем
    await asyncio.sleep(total_time)
    
    # Удаляем сообщение, обращаясь к .message_id
    try:
        await message.ctx_api.messages.delete(
            message_ids=[int(sent_msg.message_id)], 
            delete_for_all=True
        )
    except Exception as e:
        print(f"Ошибка удаления слов: {e}")
        
    await message.answer("Начинаем!")
    
    contents = list()
    for item in content.keys():
        contents.append((str(item).capitalize(), content[item].capitalize()))
        
    await give_case(message, contents, 0)