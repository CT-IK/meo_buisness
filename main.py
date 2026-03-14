import asyncio, logging, json, random
from aiogram import F, Bot, Dispatcher, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

from credentials import bot_token

bot = Bot(token=bot_token)
dp = Dispatcher()
router = Router()

class AdminMessage(StatesGroup):
    admin_id = State()
    send = State()
    team_id = State()

class UserMessage(StatesGroup):
    send = State()
    team_id = State()
    team_name = State()

class Registration(StatesGroup):
    name = State()
    id = State()

class Password(StatesGroup):
    passwd = State()
    id = State()
    turn = State()

class Buy(StatesGroup):
    metall = State()
    name = State()
    turn = State()
    amount = State()

class Sell(StatesGroup):
    dictmet = State()
    metall = State()
    name = State()
    turn = State()
    amount = State()

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
            print(name)
            role = info['role']
            isuser = True

    if isuser:
        if role == "admin":

            #todo сделать replykeyboard. Начать игру - зеленым
            admin_panel = InlineKeyboardBuilder()
            admin_panel.button(text="Начать игру!", callback_data="start", style="success")
            admin_panel.button(text="Статистика", callback_data=f"stat_{message.from_user.id}")
            admin_panel.button(text="Организаторы", callback_data=f"orgs_{message.from_user.id}")
            admin_panel.button(text="Отправить сообщение", callback_data=f"mes_{message.from_user.id}")
            admin_panel.adjust(1,2,1,1)


            await message.answer(f"Добро пожаловать, {name}!", reply_markup=admin_panel.as_markup())
        else:
            #todo сделать replykeyboard. ГОТОВО - зеленым (удалять кнопку при использовании)
            ready = InlineKeyboardBuilder()
            ready.button(text="Состояние портфеля", callback_data=f"finance_{name}_1")
            ready.button(text="Техподдержка", callback_data=f"help_{name}")
            ready.button(text="ГОТОВ!", callback_data=f"user_ready_{name}", style="success")
            ready.adjust(2,1)

            await message.answer(f"Добро пожаловать, команда {name}!\n\nНажмите ГОТОВ, если ваша команда готова к игре", reply_markup=ready.as_markup())

    else:
        reg = InlineKeyboardBuilder()
        reg.button(text="Начать регистрацию!", callback_data="reg")

        await message.answer("Добро пожаловать на Бизнес-монополию!\n\nК сожалению, не нашел вас в своей базе(\n\nНачнём регистрацию?", reply_markup=reg.as_markup())

@dp.callback_query(F.data == "reg")
async def registration(callback: CallbackQuery, state: FSMContext):
    try:
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

            #todo тоже самое. Сделать ГОТОВ! зелёным
            ready = InlineKeyboardBuilder()
            ready.button(text="Состояние портфеля", callback_data=f"finance_{name}_1")
            ready.button(text="Техподдержка", callback_data=f"help_{name}")
            ready.button(text="ГОТОВ!", callback_data=f"user_ready_{name}", style="success")
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

    for i in range(len(data)):
        if list(data.values())[i]['role'] == "admin":
            identificator = list(data.values())[i]['tg_id']
            #todo ReplyKeyboard Завершить раунд - красным
            admin_panel_game = InlineKeyboardBuilder()
            admin_panel_game.button(text="Статистика", callback_data=f"stat_{callback.from_user.id}")
            admin_panel_game.button(text="Организаторы", callback_data=f"orgs_{callback.from_user.id}")
            admin_panel_game.button(text="Отправить сообщение", callback_data=f"mes_{callback.from_user.id}")
            admin_panel_game.button(text="Завершить раунд", callback_data="admin_end_round", style="danger")
            admin_panel_game.adjust(2, 1, 1)

            await bot.send_message(chat_id=identificator, text="Игра началась. Нужно дать код игрокам", reply_markup=admin_panel_game.as_markup())

@dp.callback_query(F.data == "round1_start")
async def round1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(id=callback.from_user.id)
    await state.update_data(turn=1)
    await callback.message.answer("Введи пароль ведущего для запуска 1 раунда")
    await state.set_state(Password.passwd)

@dp.callback_query(F.data == "round_start")
async def round(callback: CallbackQuery, state: FSMContext):

    with open('data.json', 'r', encoding='utf-8') as rf:
        data = json.load(rf)
    rf.close()

    turn = 0
    try:
        for k, v in data.items():
            if str(v.get('tg_id')) == str(callback.from_user.id):
                turn = int(v.get('round_turn')) + 1
                break
    except Exception as e:
        print(e)

    print(turn)

    if int(turn) == 6:

        for i in range(len(data)):
            if list(data.values())[i]['role'] == "team":
                ident = list(data.values())[i]['tg_id']
                name = list(data.values())[i]['name']

                #todo ReplyKeyboard
                finish = InlineKeyboardBuilder()
                finish.button(text="Просмотреть свои результаты", callback_data=f"finance_{name}_5")

                await bot.send_message(chat_id=ident,
                                       text="Администратор запускает игру! Нажимай Ввести код и вводи код от ведущего",
                                       reply_markup=finish.as_markup())
    else:
        await callback.answer()
        await state.update_data(id=callback.from_user.id)
        await state.update_data(turn=turn)
        await callback.message.answer(f"Введи пароль ведущего для запуска {turn} раунда")
        await state.set_state(Password.passwd)

@dp.message(Password.passwd)
async def password_check(message: Message, state: FSMContext):
    #todo поменять пароли на более сложные
    password_list = ["market26", "round62", "trA2de6", "pr6ofITe2", "F1na1"]
    data = await state.get_data()
    user_id = data.get("id")
    turn = data.get("turn")
    user_password = int(message.text)

    check_password = password_list[turn - 1]

    if user_password == check_password:

        with open('data.json', 'r', encoding='utf-8') as rf:
            data = json.load(rf)
        rf.close()

        name = ''
        try:
            for k, v in data.items():
                if str(v.get('tg_id')) == str(user_id):
                    name = str(v.get('name'))
                    v['round_turn'] = int(turn)
                    break
        except Exception as e:
            print(e)

        with open('data.json', 'w', encoding='utf-8') as wf:
                json.dump(data, wf, ensure_ascii=False, indent=4)

        # todo ReplyKeyboard Завершить раунд - красным
        gamer = InlineKeyboardBuilder()
        gamer.button(text="Купить актив", callback_data=f"buy_{name}_{turn}")
        gamer.button(text="Продать актив", callback_data=f"sell_{name}_{turn}")
        gamer.button(text="Рынок", callback_data=f"stock_{turn}")
        gamer.button(text="Состояние портфеля", callback_data=f"finance_{name}_{turn}")
        gamer.button(text="Техподдержка", callback_data=f"help_{name}")
        gamer.button(text="Завершить раунд", callback_data=f"end_round_{name}_{turn}", style="danger")
        gamer.adjust(2,2,1,1)

        await bot.send_message(chat_id=user_id, text=f"Добро пожаловать в {turn} раунд!\n\nHappy Hunger Games! And may the odds be ever in your favor", reply_markup=gamer.as_markup())
        await state.clear()

    else:
        if turn > 1:
            approve = InlineKeyboardBuilder()
            approve.button(text="Ввести код заново", callback_data="round1_start")
            await bot.send_message(chat_id=user_id, text="Пароль неверный! Попробуй ещё раз", reply_markup=approve.as_markup())
            await state.clear()
        else:
            approve = InlineKeyboardBuilder()
            approve.button(text="Ввести код заново", callback_data="round_start")
            await bot.send_message(chat_id=user_id, text="Пароль неверный! Попробуй ещё раз",
                                   reply_markup=approve.as_markup())
            await state.clear()

@dp.callback_query(F.data[:10] == "end_round_")
async def user_end(callback: CallbackQuery):
    callback_data = str(callback.data)
    name = callback_data[10:-2]
    turn = callback_data[-1]

    #todo сделать Да - зеленым, а Нет - красным
    approve = InlineKeyboardBuilder()
    approve.button(text="Да", callback_data=f"user_end_prov_{name}_{turn}", style="success")
    approve.button(text="Нет", callback_data=f"user_end_decl_{name}_{turn}", style="danger")
    await bot.send_message(chat_id=callback.from_user.id, text="Вы уверены, что хотите завершить раунд? Вы перейдете в окно ожидания, а операции в этом раунде будут невозможны", reply_markup=approve.as_markup())

@dp.callback_query(F.data[:14] == "user_end_prov_")
async def user_end_prov(callback: CallbackQuery):
    callback_data = str(callback.data)
    name = callback_data[14:-2]
    turn = callback_data[-1]

    await bot.send_message(chat_id=callback.from_user.id, text="Ожидайте начала следующего раунда")
    await bot.send_message(chat_id=1068689003, text=f"Команда {name} завершила {turn} раунд")

@dp.callback_query(F.data[:14] == "user_end_decl_")
async def user_end_decl(callback: CallbackQuery):
    callback_data = str(callback.data)
    name = callback_data[14:-2]
    turn = callback_data[-1]

    #todo всё тоже самое, что и с обычной клавиатурой пользователя
    gamer = InlineKeyboardBuilder()
    gamer.button(text="Купить актив", callback_data=f"buy_{name}_{turn}")
    gamer.button(text="Продать актив", callback_data=f"sell_{name}_{turn}")
    gamer.button(text="Рынок", callback_data=f"stock_{turn}")
    gamer.button(text="Состояние портфеля", callback_data=f"finance_{name}_{turn}")
    gamer.button(text="Техподдержка", callback_data=f"help_{name}")
    gamer.button(text="Завершить раунд", callback_data=f"end_round_{name}_{turn}", style="danger")
    gamer.adjust(2, 2, 1, 1)

    await bot.send_message(chat_id=callback.from_user.id, text="Завершение раунда отменено!", reply_markup=gamer.as_markup())

@dp.callback_query(F.data[:15] == "admin_end_round")
async def admin_end(callback: CallbackQuery):
    try:
        print(callback.from_user.id)
        with open('data.json', 'r', encoding='utf-8') as rf:
            data = json.load(rf)
        rf.close()

        approve = InlineKeyboardBuilder()
        approve.button(text="Ввести код для следующего раунда", callback_data="round_start")

        for i in range(len(data)):
            if list(data.values())[i]['role'] == "team":
                ident = list(data.values())[i]['tg_id']

                await bot.send_message(chat_id=ident,
                                       text="Раунд был завершен администратором! Надеюсь ты все успел... Готов приступить к следующему раунду?",
                                       reply_markup=approve.as_markup())

        for i in range(len(data)):
            if list(data.values())[i]['role'] == "admin":
                identificator = list(data.values())[i]['tg_id']
                # todo всё тоже самое, что и с обычной клавиатурой админа
                admin_panel_game = InlineKeyboardBuilder()
                admin_panel_game.button(text="Статистика", callback_data=f"stat_{callback.from_user.id}")
                admin_panel_game.button(text="Организаторы", callback_data=f"orgs_{callback.from_user.id}")
                admin_panel_game.button(text="Отправить сообщение", callback_data=f"mes_{callback.from_user.id}")
                admin_panel_game.button(text="Завершить раунд", callback_data="admin_end_round", style="danger")
                admin_panel_game.adjust(2, 1, 1)

                await bot.send_message(chat_id=identificator, text="Начинаем следующий раунд. Нужно дать код игрокам",
                                       reply_markup=admin_panel_game.as_markup())

    except Exception as e:
        print(e)

@dp.callback_query(F.data[:4] == "buy_")
async def buy_process(callback: CallbackQuery):
    try:
        callback_data = str(callback.data)
        name = callback_data[4:-2]
        turn = callback_data[-1]

        buy_metalls = InlineKeyboardBuilder()
        buy_metalls.button(text="Золото", callback_data=f"metall_0_{name}_{turn}")
        buy_metalls.button(text="Серебро", callback_data=f"metall_1_{name}_{turn}")
        buy_metalls.button(text="Платина", callback_data=f"metall_2_{name}_{turn}")
        buy_metalls.button(text="Палладий", callback_data=f"metall_3_{name}_{turn}")
        buy_metalls.button(text="Медь", callback_data=f"metall_4_{name}_{turn}")
        buy_metalls.button(text="Литий", callback_data=f"metall_5_{name}_{turn}")
        buy_metalls.button(text="Кобальт", callback_data=f"metall_6_{name}_{turn}")
        buy_metalls.button(text="Редкоземельные металлы", callback_data=f"metall_7_{name}_{turn}")
        buy_metalls.button(text="Железная руда", callback_data=f"metall_8_{name}_{turn}")
        buy_metalls.button(text="Алюминий", callback_data=f"metall_9_{name}_{turn}")
        buy_metalls.adjust(3,3,1,1,2)
        await bot.send_message(chat_id=callback.from_user.id, text="Выберите актив, который вы хотите купить", reply_markup=buy_metalls.as_markup())

    except Exception as e:
        print(e)

@dp.callback_query(F.data[:7] == "metall_")
async def buy_amount(callback: CallbackQuery, state: FSMContext):
    try:
        callback_data = str(callback.data)
        data = callback_data.split("_")

        await callback.answer()
        await state.update_data(metall=str(data[1]))
        await state.update_data(name=str(data[2]))
        await state.update_data(turn=str(data[3]))
        await callback.message.answer(f"Введи количество единиц металла для покупки (целое число)")
        await state.set_state(Buy.amount)

    except Exception as e:
        print(e)

@dp.message(Buy.amount)
async def buy(message: Message, state: FSMContext):
    try:
        information = await state.get_data()
        amount = message.text
        metall = information.get("metall")
        name = information.get("name")
        turn = str(information.get("turn"))

        round_info = take_round_info(turn)
        metal_cost = 0
        balance = 0
        tg_id = 0
        for i in range(len(round_info)):
            if int(metall) == i:
                metal_cost = int(list(round_info.values())[i]['Купля'])

        with open('data.json', 'r', encoding='utf-8') as rf:
            data = json.load(rf)
        rf.close()

        for i in range(len(data)):
            if list(data.values())[i]['name'] == str(name):
                tg_id = int(list(data.values())[i]['tg_id'])
                balance = int(list(data.values())[i]['balance'])

        buy_price = int(amount) * int(metal_cost)

        if balance < buy_price:
            await bot.send_message(chat_id=tg_id, text=f"К сожалению, вам не хватает {buy_price - balance} олимпов для покупки.\n\n Ваш текущий баланс: {balance} олимпов")

        else:
            balance = balance - buy_price
            metal_amount = []

            for i in range(len(data)):
                if list(data.values())[i]['name'] == str(name):
                    metal_amount += [int(list(data.values())[i]['gold']),
                                     int(list(data.values())[i]['silver']),
                                     int(list(data.values())[i]['platinum']),
                                     int(list(data.values())[i]['palladium']),
                                     int(list(data.values())[i]['cuprum']),
                                     int(list(data.values())[i]['lithium']),
                                     int(list(data.values())[i]['cobalt']),
                                     int(list(data.values())[i]['rare_metals']),
                                     int(list(data.values())[i]['iron']),
                                     int(list(data.values())[i]['aluminium'])]

            for i in range(len(metal_amount)):
                if int(metall) == int(i):
                    metal_amount[i] += int(amount)

            metal_cost = []
            for i in range(len(round_info)):
                metal_cost.append(int(list(round_info.values())[i]['Продажа']))

            total_balance = balance + sum([x * y for x, y in zip(metal_amount, metal_cost)])

            # todo сделать replykeyboard новое БЕЗ продажи/купли
            await bot.send_message(chat_id=tg_id,
                                   text=f"Транзакция завершена успешно!\n"
                                        f"Состояние портфеля команды {name}:\n\n"
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


            for k, v in data.items():
                if str(v.get('tg_id')) == str(tg_id):
                    v['balance'] = int(balance)
                    keys_list = list(v.keys())
                    key = ''
                    for i in range(len(keys_list)):
                        if i == int(metall) + 5:
                           key = str(keys_list[i])
                    v[key] = str(metal_amount[int(metall)])
                    break

            with open('data.json', 'w', encoding='utf-8') as wf:
                json.dump(data, wf, ensure_ascii=False, indent=4)


    except Exception as e:
        print(e)

@dp.callback_query(F.data[:5] == "sell_")
async def sell_process(callback: CallbackQuery, state: FSMContext):
    try:
        callback_data = str(callback.data)
        name = callback_data[5:-2]
        turn = callback_data[-1]

        with open('data.json', 'r', encoding='utf-8') as rf:
            data = json.load(rf)
        rf.close()

        metal_amount = []
        for i in range(len(data)):
            if list(data.values())[i]['name'] == str(name):
                metal_amount += [int(list(data.values())[i]['gold']),
                                 int(list(data.values())[i]['silver']),
                                 int(list(data.values())[i]['platinum']),
                                 int(list(data.values())[i]['palladium']),
                                 int(list(data.values())[i]['cuprum']),
                                 int(list(data.values())[i]['lithium']),
                                 int(list(data.values())[i]['cobalt']),
                                 int(list(data.values())[i]['rare_metals']),
                                 int(list(data.values())[i]['iron']),
                                 int(list(data.values())[i]['aluminium'])]

        idents = [0,1,2,3,4,5,6,7,8,9]
        dict_of_metals = dict(zip(idents, metal_amount))
        dict_of_metals = {k: v for k, v in dict_of_metals.items() if v != 0}


        sell_metalls = InlineKeyboardBuilder()
        for k in range(len(list(dict_of_metals.keys()))):
            if list(dict_of_metals.keys())[k] == 0:
                sell_metalls.button(text="Золото", callback_data=f"sellamount_0_{name}_{turn}")
            elif list(dict_of_metals.keys())[k] == 1:
                sell_metalls.button(text="Серебро", callback_data=f"sellamount_1_{name}_{turn}")
            elif list(dict_of_metals.keys())[k] == 2:
                sell_metalls.button(text="Платина", callback_data=f"sellamount_2_{name}_{turn}")
            elif list(dict_of_metals.keys())[k] == 3:
                sell_metalls.button(text="Палладиум", callback_data=f"sellamount_3_{name}_{turn}")
            elif list(dict_of_metals.keys())[k] == 4:
                sell_metalls.button(text="Медь", callback_data=f"sellamount_4_{name}_{turn}")
            elif list(dict_of_metals.keys())[k] == 5:
                sell_metalls.button(text="Литиум", callback_data=f"sellamount_5_{name}_{turn}")
            elif list(dict_of_metals.keys())[k] == 6:
                sell_metalls.button(text="Кобальт", callback_data=f"sellamount_6_{name}_{turn}")
            elif list(dict_of_metals.keys())[k] == 7:
                sell_metalls.button(text="Редкоземельные металлы", callback_data=f"sellamount_7_{name}_{turn}")
            elif list(dict_of_metals.keys())[k] == 8:
                sell_metalls.button(text="Железная руда", callback_data=f"sellamount_8_{name}_{turn}")
            elif list(dict_of_metals.keys())[k] == 9:
                sell_metalls.button(text="Алюминий", callback_data=f"sellamount_9_{name}_{turn}")

        await state.update_data(dictmet=dict_of_metals)
        await bot.send_message(chat_id=callback.from_user.id, text="Выберите актив, который вы хотите продать",
                               reply_markup=sell_metalls.as_markup())

    except Exception as e:
        print(e)

@dp.callback_query(F.data[:11] == "sellamount_")
async def sell_amount(callback: CallbackQuery, state: FSMContext):
    try:
        callback_data = str(callback.data)
        data = callback_data.split("_")

        await callback.answer()
        await state.update_data(metall=str(data[1]))
        await state.update_data(name=str(data[2]))
        await state.update_data(turn=str(data[3]))
        await callback.message.answer(f"Введи количество единиц металла для продажи (целое число)")
        await state.set_state(Sell.amount)

    except Exception as e:
        print(e)

@dp.message(Sell.amount)
async def sell(message: Message, state: FSMContext):
    try:
        information = await state.get_data()
        amount = message.text
        metall = information.get("metall")
        name = information.get("name")
        turn = str(information.get("turn"))
        dictmet = information.get("dictmet")

        user_amount = 0
        for k, v in dictmet.items():
            if int(k) == int(metall):
                user_amount = int(v)

        with open('data.json', 'r', encoding='utf-8') as rf:
            data = json.load(rf)
        rf.close()

        balance = 0
        tg_id = 0
        for i in range(len(data)):
            if list(data.values())[i]['name'] == str(name):
                tg_id = int(list(data.values())[i]['tg_id'])
                balance = int(list(data.values())[i]['balance'])

        if int(user_amount) < int(amount):
            await bot.send_message(chat_id=tg_id,
                                   text=f"К сожалению, вы не можете продать {amount} шт. активов.\n\n Ваш текущий баланс: {user_amount} шт.")

        else:

            round_info = take_round_info(turn)
            metal_cost = 0
            for i in range(len(round_info)):
                if int(metall) == i:
                    metal_cost = int(list(round_info.values())[i]['Продажа'])


            sell_price = int(amount) * int(metal_cost)

            balance = balance + sell_price
            metal_amount = []

            for i in range(len(data)):
                if list(data.values())[i]['name'] == str(name):
                    metal_amount += [int(list(data.values())[i]['gold']),
                                     int(list(data.values())[i]['silver']),
                                     int(list(data.values())[i]['platinum']),
                                     int(list(data.values())[i]['palladium']),
                                     int(list(data.values())[i]['cuprum']),
                                     int(list(data.values())[i]['lithium']),
                                     int(list(data.values())[i]['cobalt']),
                                     int(list(data.values())[i]['rare_metals']),
                                     int(list(data.values())[i]['iron']),
                                     int(list(data.values())[i]['aluminium'])]

            for i in range(len(metal_amount)):
                if int(metall) == int(i):
                    metal_amount[i] -= int(amount)

            metal_cost_list = []
            for i in range(len(round_info)):
                metal_cost_list.append(int(list(round_info.values())[i]['Продажа']))

            total_balance = balance + sum([x * y for x, y in zip(metal_amount, metal_cost_list)])
            print(metal_amount)
            #todo сделать replykeyboard новое БЕЗ продажи/купли
            await bot.send_message(chat_id=tg_id,
                                   text=f"Транзакция завершена успешно!\n"
                                        f"Состояние портфеля команды {name}:\n\n"
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


            for k, v in data.items():
                if str(v.get('tg_id')) == str(tg_id):
                    v['balance'] = int(balance)
                    keys_list = list(v.keys())
                    key = ''
                    for i in range(len(keys_list)):
                        if i == int(metall) + 5:
                           key = str(keys_list[i])
                    v[key] = str(metal_amount[int(metall)])
                    break

            with open('data.json', 'w', encoding='utf-8') as wf:
                json.dump(data, wf, ensure_ascii=False, indent=4)


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
                metal_amount += [int(list(data.values())[i]['gold']),
                        int(list(data.values())[i]['silver']),
                        int(list(data.values())[i]['platinum']),
                        int(list(data.values())[i]['palladium']),
                        int(list(data.values())[i]['cuprum']),
                        int(list(data.values())[i]['lithium']),
                        int(list(data.values())[i]['cobalt']),
                        int(list(data.values())[i]['rare_metals']),
                        int(list(data.values())[i]['iron']),
                        int(list(data.values())[i]['aluminium'])]

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
        #todo сделать форматирование, как то, что я присылал
        text += f"<b>{i+1}. {list(round_info.keys())[i]}:</b> <u>Купля:</u> {list(round_info.values())[i]['Купля']}, <u>Продажа:</u> {list(round_info.values())[i]['Продажа']}\n"

    await bot.send_message(chat_id=callback.from_user.id, text=text, parse_mode = "HTML")

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

    turn = 0
    for i in range(len(data)):
        if list(data.values())[i]['role'] == "team":
            turn = list(data.values())[i]['turn']
            if turn == 0:
                turn = 1
            break

    print(turn)
    round_info = take_round_info(turn)

    metal_cost = []
    for i in range(len(round_info)):
        metal_cost.append(int(list(round_info.values())[i]['Продажа']))

    for i in range(len(data)):
        if list(data.values())[i]['role'] == "team":
            metal_amount = []
            metal_amount += [int(list(data.values())[i]['gold']),
                             int(list(data.values())[i]['silver']),
                             int(list(data.values())[i]['platinum']),
                             int(list(data.values())[i]['palladium']),
                             int(list(data.values())[i]['cuprum']),
                             int(list(data.values())[i]['lithium']),
                             int(list(data.values())[i]['cobalt']),
                             int(list(data.values())[i]['rare_metals']),
                             int(list(data.values())[i]['iron']),
                             int(list(data.values())[i]['aluminium'])]

            await bot.send_message(chat_id=id, text=f"Команда: {list(data.values())[i]['name']}\n"
                                                    f"Олимпкоины: {list(data.values())[i]['balance']}\n"
                                                    f"Общий баланс:{int(list(data.values())[i]['balance']) + sum([x * y for x, y in zip(metal_amount, metal_cost)])}"
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

@dp.callback_query(F.data[:5] == "help_")
async def help(callback: CallbackQuery, state: FSMContext):
    try:
        callback_data = str(callback.data)
        team_name = callback_data[5:]
        team_id = callback.from_user.id

        await callback.answer()
        await state.update_data(team_name=team_name)
        await state.update_data(team_id=team_id)
        await callback.message.answer("Отправь сообщение")
        await state.set_state(UserMessage.send)

    except Exception as e:
        print(e)

@dp.message(UserMessage.send)
async def help_send(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        name = data.get("team_name")
        id = data.get("team_id")
        user_text = message.text

        await bot.send_message(chat_id=1068689003, text=f"Сообщение от команды {name}: {user_text}")
        await state.clear()
        await bot.send_message(chat_id=id, text="Сообщение было успешно доставлено администратору!")
    except Exception as e:
        print(e)

async def main():
    logging.basicConfig(level=logging.INFO,
                        handlers=[logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')]
                        )
    await dp.start_polling(bot)

asyncio.run(main())