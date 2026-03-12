import asyncio, logging, json, random
from aiogram import F, Bot, Dispatcher
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

from credentials import bot_token

bot = Bot(token=bot_token)
dp = Dispatcher()

class AdminMessage(StatesGroup):
    send = State()

class Registration(StatesGroup):
    name = State()

@dp.message(Command("start"))
async def start_cmd(message: Message):
    with open('data.json', 'r', encoding='utf-8') as rf:
        data = json.load(rf)
    rf.close()

    isuser = False
    name = ''
    role = ''
    for id, info in data.items():
        if str(info['tg_id']) == str(message.from_user.id):
            name = info['name']
            role = info['role']
            isuser = True

    if isuser:
        if role == "admin":
            admin_panel = ReplyKeyboardBuilder()
            admin_panel.button(text="Начать игру!", callback_data="start")
            admin_panel.button(text="Статистика", callback_data=f"stat_{message.from_user.id}")
            admin_panel.button(text="Организаторы", callback_data=f"orgs_{message.from_user.id}")
            admin_panel.button(text="Отправить сообщение", callback_data=f"mes_{message.from_user.id}")
            admin_panel.adjust(1,2,1)

            await message.answer(f"Добро пожаловать, {name}!", reply_markup=admin_panel.as_markup())
        else:
            ready = InlineKeyboardBuilder()
            ready.button(text="Состояние команды", callback_data=f"finance_{name}")
            ready.button(text="Техподдержка", callback_data=f"help_{name}")
            ready.button(text="ГОТОВ!", callback_data=f"user_ready_{name}")
            ready.adjust(1,1)

            await message.answer(f"Добро пожаловать, команда {name}!\n\nНажмите ГОТОВ, если ваша команда готова к игре", reply_markup=ready.as_markup())

    else:
        reg = InlineKeyboardBuilder()
        reg.button(text="Начать регистрацию!", callback_data="reg")

        await message.answer("Добро пожаловать на Бизнес-монополию!\n\nК сожалению, не нашел вас в своей базе(\n\nНачнём регистрацию?", reply_markup=reg.as_markup())

@dp.callback_query(F.data == "reg")
async def registration(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(id=callback.from_user.id)
    await callback.message.answer("Напиши название вашей команды")
    await state.set_state(Registration.name)


@dp.message(Registration.name)
async def get_name(message: Message, state: FSMContext):
    try:
        name = message.text
        data = await state.get_data()
        id = data.get("id")

        with open('data.json', 'r', encoding='utf-8') as rf:
            data = json.load(rf)
        rf.close()

        unique = True
        for i in range(len(data)):
            if list(data.values())[i]['role'] == "team":
                if name == list(data.values())[i]['name']:
                    unique = False
        if unique:
            # {f"{random.randint(1, 50)}"}

            team_first_part = {
                "tg_id": str(id),
                "role": "team",
                "name": str(name),
                "round_turn": "0",
                "balance": "5000"
            }
            team_second_part = {
                "gold": 0,
                "silver": 0,
                "platinum": 0,
                "palladium": 0,
                "cuprum": 0,
                "lithium": 0,
                "cobalt": 0,
                "rare_metals": 0,
                "iron": 0,
                "aluminium": 0
            }
            first_metall_id = random.randint(0, 9)
            second_metall_id = random.randint(0, 9)

            while second_metall_id == first_metall_id:
                second_metall_id = random.randint(0, 9)

            for i in range(len(team_second_part)):
                if first_metall_id == i:
                    key = list(team_second_part.keys())[i]
                    team_second_part[key] = 1
                else:
                    if second_metall_id == i:
                        key_2 = list(team_second_part.keys())[i]
                        team_second_part[key_2] = 1
            new_team_values = team_first_part | team_second_part

            new_team = {
                f"{random.randint(5, 50)}": new_team_values
            }

            data = data | new_team

            with open('data.json', 'w') as wf:
                json.dump(data, wf)
            wf.close()

            ready = InlineKeyboardBuilder()
            ready.button(text="Состояние команды", callback_data=f"finance_{name}")
            ready.button(text="Техподдержка", callback_data=f"help_{name}")
            ready.button(text="ГОТОВ!", callback_data=f"user_ready_{name}")
            ready.adjust(2,1)

            await bot.send_message(chat_id=id, text="Поздравляю с успешной регистрацией!\n\nНажмите ГОТОВ, если ваша команда готова к игре", reply_markup=ready.as_markup())


        else:
            reg = InlineKeyboardBuilder()
            reg.button(text="Записать новое имя команды", callback_data="reg")
            await bot.send_message(chat_id=id, text="К сожалению, это имя уже занято(", reply_markup=reg.as_markup())

    except Exception as e:
        print(e)

@dp.callback_query(F.data[:11] == "user_ready_")
async def ready(callback: CallbackQuery):
    callback_data = str(callback.data)
    name = callback_data[11:]

    with open('data.json', 'r', encoding='utf-8') as rf:
        data = json.load(rf)
    rf.close()

    admins = []
    for id, info in data.items():
        if str(info['role']) == "admin":
            admins.append(info["tg_id"])

    for i in range(len(admins) - 1):
        await bot.send_message(chat_id=admins[i], text=f"Команда {name} готова")


@dp.callback_query(F.data[:5] == "stat_")
async def stat(callback: CallbackQuery):
    callback_data = str(callback.data)
    id = callback_data[5:]
    with open('data.json', 'r', encoding='utf-8') as rf:
        data = json.load(rf)
    rf.close()


    for i in range(len(data)):
        if list(data.values())[i]['role'] == "team":
            await bot.send_message(chat_id=id, text=f"Команда: {list(data.values())[i]['name']}\n"
                                                    f"Олимпкоины: {list(data.values())[i]['balance']}\n"
                                                    f"Золото: {list(data.values())[i]['gold']}\n"
                                                    f"Серебро: {list(data.values())[i]['silver']}\n"
                                                    f"Платина: {list(data.values())[i]['platinum']}\n"
                                                    f"Палладий: {list(data.values())[i]['palladium']}\n"
                                                    f"Медь: {list(data.values())[i]['cuprum']}\n"
                                                    f"Литий: {list(data.values())[i]['lithium']}\n"
                                                    f"Кобальт: {list(data.values())[i]['cobalt']}\n"
                                                    f"Редкоземельные металлы: {list(data.values())[i]['rare_metals']}\n"
                                                    f"Железная руда: {list(data.values())[i]['iron']}\n"
                                                    f"Алюминий: {list(data.values())[i]['aluminium']}\n")

@dp.callback_query(F.data[:5] == "orgs_")
async def orgs(callback: CallbackQuery):
    callback_data = str(callback.data)
    id = callback_data[5:]

    with open('data.json', 'r', encoding='utf-8') as rf:
        data = json.load(rf)
    rf.close()

    admins = []
    for i in range(len(data)):
        if list(data.values())[i]['role'] == "admin":
            print('hui')
            try:
                username = await bot.get_chat(int(list(data.values())[i]["tg_id"]))
                admins.append(f"{list(data.values())[i]["name"]} {"@" + str(username.username)}")
            except Exception:
                admins.append(f"{list(data.values())[i]["name"]}")
            print(admins)

    text = "Список организаторов:\n"
    for i in range(len(admins)):
        text += f"{admins[i]}\n"

    await bot.send_message(chat_id=id, text=text)

@dp.callback_query(F.data[:4] == "mes_")
async def message(callback: CallbackQuery, state: FSMContext):
    callback_data = str(callback.data)
    id = callback_data[4:]
    opt_team = InlineKeyboardBuilder()

    with open('data.json', 'r', encoding='utf-8') as rf:
        data = json.load(rf)
    rf.close()

    for i in range(len(data)):
        if list(data.values())[i]['role'] == "team":
            opt_team.button(text=f"{list(data.values())[i]['name']}",
                            callback_data=f"send_message_{list(data.values())[i]['tg_id']}")
    opt_team.button(text="Всем командам", callback_data="send_message_all")


    await state.update_data(admin_id=id)
    await bot.send_message(chat_id=id,
                           text="Выбери команду, которой будет отправлено сообщение",
                           reply_markup=opt_team.as_markup())

@dp.callback_query(F.data[:13] == "send_message_")
async def send_message(callback: CallbackQuery, state: FSMContext):
    try:
        callback_data = str(callback.data)
        team_ident = callback_data[13:]

        with open('data.json', 'r', encoding='utf-8') as rf:
            data = json.load(rf)
        rf.close()

        if team_ident == "all":
            print("huila")
            team = []
            for i in range(len(data)):
                if list(data.values())[i]['role'] == "team":
                    team.append(str(list(data.values())[i]['tg_id']))
        else:
            team = team_ident

        await callback.answer()
        await state.update_data(team_id=team)
        await callback.message.answer("Отправь сообщение")
        await state.set_state(AdminMessage.send)

    except Exception as e:
        print(e)


@dp.message(AdminMessage.send)
async def send(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        id = data.get("team_id")
        user_text = message.text
        admin_id = data.get("admin_id")

        if type(id) == list:
            for i in range(len(id)):
                await bot.send_message(chat_id=id[i], text=user_text)
        else:
            await bot.send_message(chat_id=int(id), text=user_text)

        await state.clear()
        await bot.send_message(chat_id=admin_id, text="Сообщение было успешно доставлено команде!")
    except Exception as e:
        print(e)


async def main():
    logging.basicConfig(level=logging.INFO,
                        handlers=[logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')]
                        )
    await dp.start_polling(bot)

asyncio.run(main())