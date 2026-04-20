from Databases.database import changes_from_user
from vkbottle import Keyboard, KeyboardButtonColor, Text
from state_manager import register_next_step

def get_keyboard(custom_markup: list=None, settings: bool=False, empty: bool=True):
    keyboard = Keyboard(one_time=False)
    if not empty:
        keyboard.add(Text("Настройки"), color=KeyboardButtonColor.SECONDARY)
        keyboard.add(Text("Далее"), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("mini app"), color=KeyboardButtonColor.SECONDARY)
        keyboard.row()
    if custom_markup:
        for btn in custom_markup:
            keyboard.add(Text(btn), color=KeyboardButtonColor.SECONDARY)
        keyboard.row()
    if settings:
        keyboard.add(Text("время -> чисел"), color=KeyboardButtonColor.SECONDARY)
        keyboard.add(Text("кол-во -> чисел"), color=KeyboardButtonColor.SECONDARY)
        keyboard.row()
        keyboard.add(Text("время -> слов"), color=KeyboardButtonColor.SECONDARY)
        keyboard.add(Text("кол-во -> слов"), color=KeyboardButtonColor.SECONDARY)
        keyboard.row()
        keyboard.add(Text("Назад"), color=KeyboardButtonColor.NEGATIVE)
    return keyboard.get_json()

async def get_changes(message, id_):
    async def process_input(field, msg):
        try:
            value = int(msg.text)
        except ValueError:
            value = 5 
        changes_from_user(id_, field, value)
        await msg.answer("Готово")

    async def another_step(msg):
        await msg.answer("Вернулись!", keyboard=get_keyboard(empty=False))

    text_lower = message.text.lower()
    
    if text_lower == "время -> чисел":
        await message.answer('Введите новое значение - сколько секунд бот будет давать на запоминание 1 числа (только число)')
        async def step1(msg):
            if msg.text.lower() == 'назад':
                await another_step(msg)
            else:
                await process_input('number_time', msg)
        register_next_step(id_, step1)
        
    elif text_lower == "кол-во -> чисел":
        await message.answer('Введите новое значение - количество чисел в тренировке (только число)')
        async def step2(msg):
            if msg.text.lower() == 'назад':
                await another_step(msg)
            else:
                await process_input('number_quantity', msg)
        register_next_step(id_, step2)
        
    elif text_lower == "время -> слов":
        await message.answer('Введите новое значение - сколько секунд бот будет давать на запоминание 1 слова (только число)')
        async def step3(msg):
            if msg.text.lower() == 'назад':
                await another_step(msg)
            else:
                await process_input('words_time', msg)
        register_next_step(id_, step3)
        
    elif text_lower == "кол-во -> слов":
        await message.answer('Введите новое значение - количество слов в тренировке (только число)')
        async def step4(msg):
            if msg.text.lower() == 'назад':
                await another_step(msg)
            else:
                await process_input('words_quantity', msg)
        register_next_step(id_, step4)
        
    else:
        await message.answer('Не понял команды')