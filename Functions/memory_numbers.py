import random
import asyncio
from Databases.database import find_user_id_by_tg_id, get_user_by_id
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
        return await message.answer("Числа закончились...")
    
    item, correct_answer = cases[case_id]
    await message.answer(f"Необходимо ответить на: {int(item) + 1}")
    
    async def next_step(msg):
        await check_case(msg, cases, case_id, correct_answer)
        
    register_next_step(message.from_id, next_step)

def make_right(list_, how_many):
    new = dict()
    for count, el in enumerate(list_):
        new[count] = f'{el}'
    return new

async def new_cmd_memo_get(message):
    user_data = list(get_user_by_id(find_user_id_by_tg_id(int(message.from_id))))
    
    count_numbers = int(user_data[3])
    time_per_number = int(user_data[2])
    
    new_numbers = [str(random.randint(0, 100)) for _ in range(count_numbers)]
    content = make_right(new_numbers, count_numbers)
    job = ' | '.join(new_numbers)
    
    sent_msg = await message.answer(f"{job}")
    
    await asyncio.sleep(time_per_number * count_numbers)
    
    try:
        await message.ctx_api.messages.delete(
            message_ids=[int(sent_msg.message_id)], 
            delete_for_all=True
        )
    except Exception as e:
        print(f"Ошибка при удалении: {e}")

    await message.answer("Начинаем!!")
    
    contents = list()
    for item in content.keys():
        contents.append((str(item).capitalize(), content[item].capitalize()))
        
    await give_case(message, contents, 0)