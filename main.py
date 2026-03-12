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
    admin_id = State()
    send = State()
    team_id = State()

class Registration(StatesGroup):
    name = State()
    id = State()

class Password(StatesGroup):
    passwd = State()
    id = State()

def take_round_info(turn):
    if turn == '1':
        with open('round_stock/round1.json', 'r', encoding='utf-8') as rf:
            round_info = json.load(rf)
        rf.close()

    elif turn == '2':
        with open('round_stock/round2.json', 'r', encoding='utf-8') as rf:
            round_info = json.load(rf)
        rf.close()

    elif turn == '3':
        with open('round_stock/round3.json', 'r', encoding='utf-8') as rf:
            round_info = json.load(rf)
        rf.close()

    elif turn == '4':
        with open('round_stock/round4.json', 'r', encoding='utf-8') as rf:
            round_info = json.load(rf)
        rf.close()

    elif turn == '5':
        with open('round_stock/round5.json', 'r', encoding='utf-8') as rf:
            round_info = json.load(rf)
        rf.close()
    return round_info

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
    #TODO переделать некоторые клавиатуры на Reply и добавить цвета
        if role == "admin":

            admin_panel = InlineKeyboardBuilder()
            admin_panel.button(text="Начать игру!", callback_data="start")
            admin_panel.button(text="Статистика", callback_data=f"stat_{message.from_user.id}")
            admin_panel.button(text="Организаторы", callback_data=f"orgs_{message.from_user.id}")
            admin_panel.button(text="Состояние портфеля", callback_data=f"finance_{name}_1")
            admin_panel.button(text="Отправить сообщение", callback_data=f"mes_{message.from_user.id}")
            admin_panel.adjust(1,2,1,1)

            await message.answer(f"Добро пожаловать, {name}!", reply_markup=admin_panel.as_markup())
        else:
            ready = InlineKeyboardBuilder()
            ready.button(text="Состояние портфеля", callback_data=f"finance_{name}")
            ready.button(text="Техподдержка", callback_data=f"help_{name}")
            ready.button(text="ГОТОВ!", callback_data=f"user_ready_{name}") #todo удалять, при использовании
            ready.adjust(2,1)

            await message.answer(f"Добро пожаловать, команда {name}!\n\nНажмите ГОТОВ, если ваша команда готова к игре", reply_markup=ready.as_markup())

    else:
        reg = InlineKeyboardBuilder()
        reg.button(text="Начать регистрацию!", callback_data="reg")

        await message.answer("Добро пожаловать на Бизнес-монополию!\n\nК сожалению, не нашел вас в своей базе(\n\nНачнём регистрацию?", reply_markup=reg.as_markup())

@dp.callback_query(F.data == "reg")
async def registration(callback: CallbackQuery, state: FSMContext):
    try:
        print('hui')
        await callback.answer()
        await state.update_data(id=callback.from_user.id)
        await callback.message.answer("Напиши название вашей команды")
        await state.set_state(Registration.name)

    except Exception as e:
        print(e)


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
            ready.button(text="Состояние портфеля", callback_data=f"finance_{name}")
            ready.button(text="Техподдержка", callback_data=f"help_{name}")
            ready.button(text="ГОТОВ!", callback_data=f"user_ready_{name}")
            ready.adjust(2,1)

            await bot.send_message(chat_id=id, text="Поздравляю с успешной регистрацией!\n\nНажмите ГОТОВ, если ваша команда готова к игре", reply_markup=ready.as_markup())
            await state.clear()


        else:
            reg = InlineKeyboardBuilder()
            reg.button(text="Записать новое имя команды", callback_data="reg")
            await bot.send_message(chat_id=id, text="К сожалению, это имя уже занято(", reply_markup=reg.as_markup())
            await state.clear()


    except Exception as e:
        print(e)

@dp.callback_query(F.data == "start")
async def start(callback: CallbackQuery):
    await bot.send_message(chat_id=callback.from_user.id, text='Игра запущена, мой господин! Да прибудет с тобой сила')

    with open('data.json', 'r', encoding='utf-8') as rf:
        data = json.load(rf)
    rf.close()

    approve = InlineKeyboardBuilder()
    approve.button(text="Ввести код", callback_data="round1_start")

    for i in range(len(data)):
        if list(data.values())[i]['role'] == "team":
            ident = list(data.values())[i]['tg_id']

            await bot.send_message(chat_id=ident,
                                   text="Администратор запускает игру! Нажимай Ввести код и вводи код от ведущего",
                                   reply_markup=approve.as_markup())

@dp.callback_query(F.data == "round1_start")
async def round1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(id=callback.from_user.id)
    await callback.message.answer("Введи пароль ведущего для запуска 1 раунда")
    await state.set_state(Password.passwd)

@dp.message(Password.passwd)
async def password_check(message: Message, state: FSMContext):
    password1 = 12345
    data = await state.get_data()
    id = data.get("id")
    user_password = int(message.text)

    if user_password == password1:

        with open('data.json', 'r', encoding='utf-8') as rf:
            data = json.load(rf)
        rf.close()

        name = ''
        for i in range(len(data)):
            if str(list(data.values())[i]['tg_id']) == str(id):
                name = list(data.values())[i]['name']

        gamer = InlineKeyboardBuilder()
        gamer.button(text="Купить актив", callback_data=f"buy_{name}")
        gamer.button(text="Продать актив", callback_data=f"sell_{name}")
        gamer.button(text="Рынок", callback_data=f"stock_1")
        gamer.button(text="Состояние портфеля", callback_data=f"finance_{name}_1")
        gamer.button(text="Техподдержка", callback_data=f"help_{name}")
        gamer.button(text="Завершить раунд", callback_data=f"end_round_{name}")

        await bot.send_message(chat_id=id, text="Добро пожаловать в первый раунд!\n\n Happy Hunger Games! And may the odds be ever in your favor", reply_markup=gamer.as_markup())
        await state.clear()

    else:
        approve = InlineKeyboardBuilder()
        approve.button(text="Ввести код заново", callback_data="round1_start")
        await bot.send_message(chat_id=id, text="Пароль неверный! Попробуй ещё раз", reply_markup=approve.as_markup())
        await state.clear()

#TODO обработка для 2 и дальнейших раундов
@dp.callback_query(F.data == "round_start")
async def round(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(id=callback.from_user.id)
    await callback.message.answer("Введи пароль ведущего для запуска 1 раунда")
    await state.set_state(Password.passwd)

#TODO обработка для 2 и дальнейших раундов
@dp.message(Password.passwd)
async def password_next_check(message: Message, state: FSMContext):
    data = await state.get_data()
    id = data.get("id")
    user_password = int(message.text)

    if user_password == password:

        with open('data.json', 'r', encoding='utf-8') as rf:
            data = json.load(rf)
        rf.close()

        name = ''
        for i in range(len(data)):
            if str(list(data.values())[i]['tg_id']) == str(id):
                name = list(data.values())[i]['name']

        gamer = InlineKeyboardBuilder()
        gamer.button(text="Купить актив", callback_data=f"buy_{name}")
        gamer.button(text="Продать актив", callback_data=f"sell_{name}")
        gamer.button(text="Рынок", callback_data=f"stock_1")
        gamer.button(text="Состояние портфеля", callback_data=f"finance_{name}_{turn}")
        gamer.button(text="Техподдержка", callback_data=f"help_{name}")
        gamer.button(text="Завершить раунд", callback_data=f"end_round_{name}")

        await bot.send_message(chat_id=id, text="Добро пожаловать в первый раунд!\n\n Happy Hunger Games! And may the odds be ever in your favor", reply_markup=gamer.as_markup())
        await state.clear()

    else:
        approve = InlineKeyboardBuilder()
        approve.button(text="Ввести код заново", callback_data="round_start")
        await bot.send_message(chat_id=id, text="Пароль неверный! Попробуй ещё раз", reply_markup=approve.as_markup())
        await state.clear()

@dp.callback_query(F.data[:4] == "buy_")
async def buy(callback: CallbackQuery):
    #TODO сделать основную обработку покупки
    try:
        callback_data = str(callback.data)
        name = callback_data[8:-2]
        turn = callback_data[-1]



    except Exception as e:
        print(e)

@dp.callback_query(F.data[:5] == "sell_")
async def sell(callback: CallbackQuery):
    # TODO сделать основную обработку продажи
    try:
        callback_data = str(callback.data)
        name = callback_data[8:-2]
        turn = callback_data[-1]



    except Exception as e:
        print(e)

@dp.callback_query(F.data[:8] == "finance_")
async def finance(callback: CallbackQuery):
    try:
        callback_data = str(callback.data)
        name = callback_data[8:-2]
        turn = callback_data[-1]

        with open('data.json', 'r', encoding='utf-8') as rf:
            data = json.load(rf)
        rf.close()

        balance = 0

        metal_amount = []
        for i in range(len(data)):
            if list(data.values())[i]['name'] == str(name):
                balance = int(list(data.values())[i]['balance'])
                gold = int(list(data.values())[i]['gold'])
                silver = int(list(data.values())[i]['silver'])
                platinum = int(list(data.values())[i]['platinum'])
                palladium = int(list(data.values())[i]['palladium'])
                cuprum = int(list(data.values())[i]['cuprum'])
                lithium = int(list(data.values())[i]['lithium'])
                cobalt = int(list(data.values())[i]['cobalt'])
                rare_metals = int(list(data.values())[i]['rare_metals'])
                iron = int(list(data.values())[i]['iron'])
                aluminium = int(list(data.values())[i]['aluminium'])
                metal_amount += [gold, silver, platinum, palladium, cuprum, lithium, cobalt, rare_metals, iron, aluminium]

        round_info = take_round_info(turn)

        metal_cost = []
        for i in range(len(round_info)):
            metal_cost.append(int(list(round_info.values())[i]['Продажа']))

        total_balance = balance + sum([x * y for x, y in zip(metal_amount, metal_cost)])

        await bot.send_message(chat_id=callback.from_user.id,
                               text=f"Состояние портфеля команды {name}:\n\n"
                                    f"Олимпкоины: {balance}\n"
                                    f"Общий баланс: {total_balance}\n"
                                    f"Золото: {metal_amount[0]} шт.\n"
                                    f"Серебро: {metal_amount[1]} шт.\n"
                                    f"Платина: {metal_amount[2]} шт.\n"
                                    f"Палладий: {metal_amount[3]} шт.\n"
                                    f"Медь: {metal_amount[4]} шт.\n"
                                    f"Литий: {metal_amount[5]} шт.\n"
                                    f"Кобальт: {metal_amount[6]} шт.\n"
                                    f"Редкоземельные металлы: {metal_amount[7]} шт.\n"
                                    f"Железная руда: {metal_amount[8]} шт.\n"
                                    f"Алюминий: {metal_amount[9]} шт.\n")
    except Exception as e:
        print(e)

@dp.callback_query(F.data[:6] == "stock_")
async def stock(callback: CallbackQuery):
    callback_data = str(callback.data)
    turn = callback_data[6:]

    round_info = take_round_info(turn)

    text = f"Состояние рынка на {turn} раунд:\n"

    for i in range(len(round_info)):
        text += f"{i+1}. {list(round_info.keys())[i]}: Купля: {list(round_info.values())[i]['Купля']}, Продажа: {list(round_info.values())[i]['Продажа']}\n"

    await bot.send_message(chat_id=callback.from_user.id, text=text)

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