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
        keyboard.add(Text("время -> чисел"))
        keyboard.add(Text("кол-во -> чисел"))
        keyboard.row()
        keyboard.add(Text("время -> слов"))
        keyboard.add(Text("кол-во -> слов"))
        keyboard.row()
        keyboard.add(Text("Язык ассоциаций"), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Назад"), color=KeyboardButtonColor.NEGATIVE)
    return keyboard.get_json()

async def get_changes(message, id_):
    async def process_input(field, msg):
        val = msg.text
        if field != 'lang_pair':
            try: val = int(msg.text)
            except: val = 5
        changes_from_user(id_, field, val)
        await msg.answer(f"Готово! Изменения сохранены.")

    text_lower = message.text.lower()
    
    if text_lower == "язык ассоциаций":
        await message.answer(
            "Введите пару языков через пробел.\n"
            "Доступно: rus, en, es\n"
            "Пример: 'rus en'"
        )
        async def step_lang(msg):
            parts = msg.text.lower().split()
            valid = ['rus', 'en', 'es']
            if len(parts) == 2 and parts[0] in valid and parts[1] in valid:
                await process_input('lang_pair', msg)
            else:
                await msg.answer("Ошибка формата. Напишите, например: rus en")
        register_next_step(id_, step_lang)

    elif text_lower == "время -> чисел":
        await message.answer('Введите время (сек) на 1 число')
        register_next_step(id_, lambda msg: process_input('number_time', msg))
    
    elif text_lower == "кол-во -> чисел":
        await message.answer('Введите количество чисел')
        register_next_step(id_, lambda msg: process_input('number_quantity', msg))
        
    elif text_lower == "время -> слов":
        await message.answer('Введите время (сек) на 1 слово')
        register_next_step(id_, lambda msg: process_input('words_time', msg))
        
    elif text_lower == "кол-во -> слов":
        await message.answer('Введите количество слов')
        register_next_step(id_, lambda msg: process_input('words_quantity', msg))
        
    else:
        # ИСПРАВЛЕНИЕ: Бот больше не молчит на левые сообщения
        await message.answer("Не понял команду. Выберите действие на клавиатуре.")