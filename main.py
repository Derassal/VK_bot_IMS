import asyncio
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, OpenLink, Text

from Functions.dictionary import get_definition
from Functions.training import training
from Functions.reading import reversed_reading, without_vowel, half_digits
from Functions.memory_numbers import new_cmd_memo_get
from Functions.associations import get_full_line

from Databases.important import give_info
from Databases.database import create_table, add_user

from Functions.user_settings import get_changes
from state_manager import steps, register_next_step


def get_keyboard(custom_markup: list=None, settings: bool=False, empty: bool=True):
    keyboard = Keyboard(one_time=False)

    if not empty:
        base_buttons = ["Настройки", "Далее", "mini app"]
        for i in range(0, len(base_buttons), 3):
            for btn in base_buttons[i:i+3]:
                keyboard.add(Text(btn))
            keyboard.row()

    if custom_markup:
        for i in range(0, len(custom_markup), 3):
            for btn in custom_markup[i:i+3]:
                keyboard.add(Text(btn))
            keyboard.row()

    if settings:
        keyboard.row()
        keyboard.add(Text("время -> чисел"))
        keyboard.add(Text("кол-во -> чисел"))

        keyboard.row()
        keyboard.add(Text("время -> слов"))
        keyboard.add(Text("кол-во -> слов"))

        keyboard.row()
        keyboard.add(Text("Назад"))

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

    if message.from_id in steps:
        func = steps.pop(message.from_id)
        await func(message)
        return

    text = message.text.lower()

    if "mini app" in text:
        keyboard = (
            Keyboard(inline=True)
            .add(OpenLink(label="Открыть mini app", link=give_info('url')))
        ).get_json()

        await message.answer("Нажми кнопку ниже:", keyboard=keyboard)
        return

    elif text == "толкование терминов":
        await message.answer(
            "Введите слово, значение которого хотите узнать",
            keyboard=get_keyboard(empty=True)
        )

        async def next_step(msg: Message):
            definition = await get_definition(msg.text)
            await reply(msg, "Определение: " + str(definition))

        register_next_step(message.from_id, next_step)

    elif text == "ассоциации":
        await message.answer(
            "Введите слово(а), ассоциацию(ии) к которому(ым) хотите получить",
            keyboard=get_keyboard(empty=True)
        )

        async def next_step(msg: Message):
            associations = await get_full_line(msg.text)
            await msg.answer(
                "Результат:\n" + "\n".join(associations), 
                keyboard=get_keyboard([
                    'Толкование терминов',
                    'Числа',
                    'Ассоциации',
                    'Скорочтение',
                    'Слова',
                    'Назад'
                ])
            )

        register_next_step(message.from_id, next_step)

    elif text == "числа":
        new_cmd_memo_get(message)

    elif text == "скорочтение":
        await message.answer(
            "Выберите раздел для тренировки",
            keyboard=get_keyboard([
                'Чтение наоборот',
                'Чтение без гласных',
                'Слова полуцифры',
                'В начало'
            ])
        )

    elif text in ["далее", "в начало"]:
        await message.answer(
            "Выберите раздел для тренировки",
            keyboard=get_keyboard([
                'Толкование терминов',
                'Числа',
                'Ассоциации',
                'Скорочтение',
                'Слова',
                'Назад'
            ])
        )

    elif text == "настройки":
        await message.answer(
            "Вы можете выбрать одну из опций",
            keyboard=get_keyboard(settings=True)
        )

    elif text == "назад":
        await reply(message, "Выберите режим работы")

    elif text == "чтение наоборот":
        await reversed_reading(message)

    elif text == "чтение без гласных":
        await without_vowel(message)

    elif text == "слова полуцифры":
        await half_digits(message)

    elif text == "слова":
        await training(message)

    else:
        await get_changes(message, message.from_id)


if __name__ == "__main__":
    bot.run_forever()