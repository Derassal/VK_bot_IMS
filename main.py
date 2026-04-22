import asyncio
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, OpenLink, Text, KeyboardButtonColor

from Functions.dictionary import get_definition
from Functions.training import training
from Functions.reading import reversed_reading, without_vowel, half_digits
from Functions.memory_numbers import new_cmd_memo_get
from Functions.associations import get_full_line

from Databases.important import give_info
from Databases.database import create_table, add_user, get_user_lang

from Functions.user_settings import get_changes
from state_manager import steps, register_next_step

# Улучшенная функция клавиатуры
def get_keyboard(custom_markup: list=None, settings: bool=False, empty: bool=True):
    keyboard = Keyboard(one_time=False)

    # 1. Базовые кнопки (если не empty)
    if not empty:
        keyboard.add(Text("Настройки"), color=KeyboardButtonColor.SECONDARY)
        keyboard.add(Text("Далее"), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("mini app"), color=KeyboardButtonColor.SECONDARY)
        keyboard.row() # Перенос строки после базы

    # 2. Кастомные кнопки из custom_markup (по 2 в ряд для красоты и стабильности)
    if custom_markup:
        for i, btn in enumerate(custom_markup):
            keyboard.add(Text(btn), color=KeyboardButtonColor.SECONDARY)
            # Если кнопка вторая в ряду или последняя в списке — делаем перенос
            if (i + 1) % 2 == 0:
                keyboard.row()
        # Если кнопок было нечетное количество, добавим перенос в конце
        if len(custom_markup) % 2 != 0:
            keyboard.row()

    # 3. Кнопки настроек
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

async def reply(msg: Message, text: str):
    await msg.answer(text, keyboard=get_keyboard(empty=False))

bot = Bot(token=give_info('token'))

@bot.on.message(text=['/start', 'старт', 'Начать'])
async def start_handler(message: Message):
    create_table()
    add_user(message.from_id, 10, 5, 10, 5)
    await reply(message, "Выберите режим работы")

@bot.on.message()
async def main_handler(message: Message):
    text = message.text.lower()

    # Анти-зависание
    if text == "отмена" and message.from_id in steps:
        steps.pop(message.from_id)
        await message.answer("Действие отменено.", keyboard=get_keyboard(empty=False))
        return

    if message.from_id in steps:
        func = steps.pop(message.from_id)
        await func(message)
        return

    if "mini app" in text:
        kb = Keyboard(inline=True).add(OpenLink(label="Открыть mini app", link=give_info('url'))).get_json()
        await message.answer("Нажми кнопку ниже:", keyboard=kb)
        return

    elif text == "толкование терминов":
        await message.answer("Введите слово:", keyboard=get_keyboard(empty=True))
        async def next_step(msg: Message):
            definition = await get_definition(msg.text)
            await reply(msg, f"Определение: {definition}")
        register_next_step(message.from_id, next_step)

    elif text == "ассоциации":
        await message.answer("Введите слово(а):", keyboard=get_keyboard(empty=True))
        async def next_step(msg: Message):
            lp = get_user_lang(msg.from_id)
            res = await get_full_line(msg.text, lp)
            await msg.answer(f"Результат ({lp}):\n" + "\n".join(res), 
                            keyboard=get_keyboard(['Толкование терминов', 'Числа', 'Ассоциации', 'Скорочтение', 'Слова', 'Назад']))
        register_next_step(message.from_id, next_step)

    elif text == "настройки":
        await message.answer("Вы можете выбрать одну из опций", keyboard=get_keyboard(settings=True))

    elif text in ["далее", "в начало"]:
        await message.answer("Выберите раздел:", 
                            keyboard=get_keyboard(['Толкование терминов', 'Числа', 'Ассоциации', 'Скорочтение', 'Слова', 'Назад']))

    elif text == "назад":
        await reply(message, "Выберите режим работы")

    elif text == "числа": await new_cmd_memo_get(message)
    elif text == "скорочтение":
        await message.answer("Раздел:", keyboard=get_keyboard(['Чтение наоборот', 'Чтение без гласных', 'Слова полуцифры', 'В начало']))
    elif text == "чтение наоборот": await reversed_reading(message)
    elif text == "чтение без гласных": await without_vowel(message)
    elif text == "слова полуцифры": await half_digits(message)
    elif text == "слова": await training(message)
    else:
        await get_changes(message, message.from_id)

if __name__ == "__main__":
    bot.run_forever()