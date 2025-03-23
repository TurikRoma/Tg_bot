from aiogram.types import Message, CallbackQuery, PreCheckoutQuery
from aiogram.enums import ChatAction
from aiogram.filters import CommandStart, Command, CommandObject, StateFilter
from aiogram import F, Router, Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from datetime import datetime

import app.keyboards as kb

from app.keyboards import create_tarif_keyboard, create_payment_type_keybord

import app.database.requests as rq

from app.generators import gpt, mental_analysis_gpt

from app.payment import send_invoice_handler

router = Router()
import asyncio





class chatStates(StatesGroup):
    set_name = State()
    set_age = State()
    set_sex = State()
    set_description_bot = State()
    mainChat = State()
    tariffsChat = State()
    profileChat = State()
    mentalAnalysisChat = State()
    startChat = State()
    generateText = State()

async def send_message(user_id, state:FSMContext, bot: Bot):
    await asyncio.sleep(240)
    current_date = datetime.now()
    response = await rq.offline(user_id, current_date)
    if response:
        await bot.send_message(chat_id=user_id, text="Вас давно не было. Как ваши дела? Может вас что то беспокоит?")
        await send_message(user_id, state, bot)
    else:
        await send_message(user_id, state, bot)

tariffs_description = {
    "Базовый" : """
Базовый тариф:
· Стоимость: 10$
· Длительность: 1 месяц
· Какое-то описание тарифа
""",
    "Продвинутый": """
Продвинутый тариф:
· Стоимость: 50$
· Длительность: 1 месяц
· Какое-то описание тарифа
""",
    "Smart": """
Smart тариф:
· Стоимость: 100$
· Длительность: 1 месяц
· Какое-то описание тарифа
"""
}

users_messages = {}
users_tariff = {}


async def get_logs(user_id,previousState:FSMContext, state, type_action):
    state_from = await previousState.get_state()
    action = ''
    if state_from == None:
        action = f'{state}'
        type_action = 'reload_bot'
    else:
        state_from = state_from.split(':')[1]
        action = f'from_{state_from}_to_{state}'
    time = datetime.now()
    await rq.set_user_log(user_id, type_action, action, time)

async def generate_text(state:FSMContext):
    response = await state.get_state()
    print(response)
    if response == "chatStates:generateText": return False
    else: return True


#--------Commands



@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, bot:Bot):
    is_generate = await generate_text(state)
    
    if is_generate:
        
        # await state.set_state(chatStates.set_name)
        user_id = message.from_user.id
        username = message.from_user.username
        if username == None:
            username = "Без имени"

        await rq.set_user(user_id, username, message.from_user.is_premium!=None)
        await message.answer("""Привет! 👋
    Добро пожаловать в наш телеграм-бот! Мы рады видеть вас здесь. 😊.
    Для дальнейшего пользования пожалуйста зарегестрируйтесь
    Вот что вы можете сделать с нашим ботом:""", reply_markup=kb.registration)
        await send_message(user_id, state, bot)
    else: 
        await message.answer('Подождите ответа...')

# ------- registration

@router.callback_query(lambda callback_query: callback_query.data == 'registration')
async def start_registration(callback_query: CallbackQuery, state:FSMContext):
    await state.set_state(chatStates.set_name)
    await callback_query.message.answer("ВВедите ваше имя:")
    await callback_query.answer()
    

@router.message(chatStates.set_name)
async def registr_set_name(message:Message, state:FSMContext):
    if message.text == None:
        await message.answer("Пожалуйста введите имя")
        return
    user_id =  message.from_user.id
    nickname = message.text
    await message.answer("Введите ваш возраст")
    await rq.set_nickname(user_id, nickname)
    await state.set_state(chatStates.set_age)

@router.message(chatStates.set_age)
async def registr_age(message:Message, state:FSMContext):
    if not message.text or not message.text.isdigit():
        await message.answer("Пожалуйста введите ваш возраст")
        return
    
    elif int(message.text) > 100:
        await message.answer("Пожалуйста введите ваш возраст")
        return
    user_id =  message.from_user.id
    age =  message.text
    await rq.set_age(user_id, age)
    await state.set_state(chatStates.set_sex)
    await message.answer("Выберите пол", reply_markup=kb.sex)

@router.callback_query(lambda callback_query: callback_query.data.startswith('sex_'))
async def registr_sex(callback_query: CallbackQuery, state:FSMContext):
    sex = callback_query.data.split('_')[1]
    user_id = callback_query.from_user.id
    await rq.set_sex(user_id, sex)
    await callback_query.message.answer("Введите как вы виде описание для бота, каким вы хотите его видеть(Можно пропустить)", reply_markup=kb.skip)
    await callback_query.answer()
    await state.set_state(chatStates.set_description_bot)


@router.message(chatStates.set_description_bot)
async def registr_set_description_bot(message:Message, state:FSMContext):
    if message.text == None:
        await message.answer("Пожалуйста введите описание для бота")
        return
    description = message.text
    user_id = message.from_user.id
    await rq.success_registration(user_id)
    await message.answer("Поздравляю вы успешно завершили регистрацию. Вот какие функции достпуспны в боте", reply_markup=kb.main)
    await rq.set_bot_description(user_id, description)
    await state.set_state(chatStates.startChat)
    


@router.callback_query(lambda callback_query: callback_query.data == 'skip')
async def skip_description_bot(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    await rq.success_registration(user_id)
    await callback_query.answer()
    await callback_query.message.answer("Поздравляю вы успешно завершили регистрацию. Вот какие функции достпуспны в боте", reply_markup=kb.main)
    await state.set_state(chatStates.startChat)
    









# ------- registration

    
@router.message(Command("chat"))
async def go_chat_cmd(message: Message, state: FSMContext, bot:Bot):
    user_id = message.from_user.id
    is_registered = await rq.is_registered(user_id)
    if not is_registered:
        await message.answer('Зарегестрируйтесь пожалуйста')
        return
    is_generate = await generate_text(state)
    if is_generate:
        
        
        await rq.check_sub(user_id)
        await get_logs(user_id, state, "mainChat", 'command')
        await state.set_state(chatStates.mainChat)
        await message.answer("Вы перешли в чат с нейронкой, напишите ей сообщение и она вам ответит!")
    else:
        await message.answer('Подождите ответа...')

@router.message(Command('tarrifs'))
async def go_chat_cmd(message: Message, state: FSMContext):
    user_id = message.from_user.id
    is_registered = await rq.is_registered(user_id)
    if not is_registered:
        await message.answer('Зарегестрируйтесь пожалуйста')
        return
    is_generate = await generate_text(state)
    if is_generate:

        await get_logs(user_id,state, "tariffsChat", 'command')

        await state.set_state(chatStates.tariffsChat)
        selected_tariff = 'Базовый'
        keyboard = create_tarif_keyboard(selected_tariff)
        await message.answer("""Базовый тариф:
        · Стоимость: 10$
        · Длительность: 1 месяц
        · Какое-то описание тарифа""", reply_markup=keyboard)
    else:
        await message.answer('Подождите ответа...')

@router.message(Command('profile'))
async def go_chat_cmd(message: Message, state: FSMContext):
    user_id = message.from_user.id
    is_registered = await rq.is_registered(user_id)
    if not is_registered:
        await message.answer('Зарегестрируйтесь пожалуйста')
        return
    is_generate = await generate_text(state)
    if is_generate:
        await rq.check_sub(user_id)
        await get_logs(user_id,state, "profileChat", 'command')

        response = await rq.get_user_sub_info(user_id)
        await state.set_state(chatStates.profileChat)
        if (response == "none"):
            await message.answer("У вас нету тарифа, пожалуйста купите тариф или воспользуйтесь другой функцией бота",
                                                reply_markup=kb.main)
        else:
            await message.answer(f"""Вот инфоормация о состоянии вашего тарифа:
Ваш индефикационный номер: {response[2]}
Ваш тариф: {response[0]}
{response[1]}""", reply_markup=kb.main)
    else: 
        await message.answer('Подождите ответа...')


@router.message(Command('mental_analysis'))
async def mental_analysis_cmd(message:Message, state: FSMContext):
    user_id = message.from_user.id
    is_registered = await rq.is_registered(user_id)
    if not is_registered:
        await message.answer('Зарегестрируйтесь пожалуйста')
        return
    await state.set_state(chatStates.mentalAnalysisChat)
    context = await rq.get_context_mental_analysis(user_id)
    response = await mental_analysis_gpt(context)

    await message.answer(response)
    await state.set_state(chatStates.mainChat)
    

@router.message(Command('refund'))
async def command_refund_handler(message: Message, bot: Bot, command: CommandObject):
    transaction_id = command.args
    try:
        await bot.refund_star_payment(
            user_id=message.from_user.id,
            telegram_payment_charge_id=transaction_id
        )
    except Exception as e:
        print(e)
# ------Commands


# ------Tariffs

@router.callback_query(lambda callback_query: callback_query.data == 'tariffs')
async def tarifs(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    await get_logs(user_id,state, "tariffsChat", 'btn')

    await state.set_state(chatStates.tariffsChat)
    selected_tariff = 'Базовый'
    keyboard = create_tarif_keyboard(selected_tariff)
    await callback_query.message.answer("""Базовый тариф:
    · Стоимость: 10$
    · Длительность: 1 месяц
    · Какое-то описание тарифа""", reply_markup=keyboard)
    await callback_query.answer()

@router.message(chatStates.tariffsChat)
async def tariffs_message(message: Message, state: FSMContext):
    if(message.successful_payment == None):
        user_id = message.from_user.id
        current_date = datetime.now()
        await message.answer('В этом чате вы не можете писать сообщения! Выберите что то из следующего списка:', 
                         reply_markup=kb.main)
        await rq.set_user_log(user_id, 'error-message', 'message outside chat', current_date)
    else:
        data = await state.get_data()
        current_date = datetime.now()
        user_id = message.from_user.id
        print(data['tariff'])
        await rq.subscribe(user_id, data['tariff'], current_date)
        await rq.set_user_log(user_id, 'payment', 'success', current_date)
        await message.answer(f'Поздравляю с успешным приобритением тарифа!', reply_markup=kb.withoutTariffs,
                              message_effect_id='5046509860389126442')
    

@router.callback_query(lambda callback_query: callback_query.data.startswith('select_'))
async def select_tarif(callback_query: CallbackQuery):
    current_text = callback_query.message.text.split(' ')[0]
    selected_tariff = callback_query.data.split('_')[1]
    if current_text != selected_tariff:
        keyboard = create_tarif_keyboard(selected_tariff)
        await callback_query.message.edit_text(f"{tariffs_description[selected_tariff]}", reply_markup=keyboard)
    await callback_query.answer()

@router.callback_query(lambda callback_query: callback_query.data == 'choose_tariff')
async def choose_tarif(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    current_date = datetime.now()
    await rq.set_user_log(user_id, 'btn', 'select_tariff', current_date)
    selected_tariff = callback_query.message.text.split(' ')[0]
    await state.set_data({"tariff": selected_tariff})
    type_payment_keybord = create_payment_type_keybord(selected_tariff)
    await callback_query.message.answer("Выберите способ оплаты:", reply_markup=type_payment_keybord)
    
    await callback_query.answer()

@router.callback_query(lambda callback_query: callback_query.data.startswith('payment_'))
async def payment_type(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    current_date = datetime.now()
    payment_type = callback_query.data.split('_')[1]

    selected_tariff = await state.get_data()
    
    await rq.set_user_log(user_id, 'payment_type', payment_type, current_date)
    await send_invoice_handler(callback_query, selected_tariff['tariff'], payment_type)
    await callback_query.answer()


@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)
        


# -------Tariffs

# -------Chat

@router.callback_query(lambda callback_query: callback_query.data == 'go_chat')
async def go_chat(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    await get_logs(user_id,state, "mainChat", 'btn')
    await rq.check_sub(user_id)
    await state.set_state(chatStates.mainChat)
    await callback_query.message.answer("Вы перешли в чат с нейронкой, напишите ей сообщение и она вам ответит!")
    await callback_query.answer()


@router.message(chatStates.generateText)
async def message_error(message: Message):
    await message.answer('Подождите ответа...')


@router.message(chatStates.mainChat)
async def mainChat_message(message: Message, state: FSMContext, bot:Bot):
    if(message.text == None):
        await message.answer("Можно вводить только текст")
    else:
        user_id = message.from_user.id
        check_sub_response = await rq.check_sub(user_id)
        amount_messages = await rq.check_amount_messages(user_id)
        is_sub = await rq.is_sub(user_id)
        if is_sub or amount_messages < 10:
            await state.set_state(chatStates.generateText)
            time_message = datetime.now()
            username = message.from_user.username
            if username == None:
                username = "без имени"
            context = await rq.get_context(user_id)
            await bot.send_chat_action(chat_id=user_id, action="typing")
            try:
                response = await asyncio.create_task(gpt(message.text, context))
                
            except:
                await message.answer("Превышенно время ожидания, попробуйте ещё раз")
                await state.set_state(chatStates.mainChat)
                return
            # gpt_response = await gpt(message.text)
            for i in range(len(response[0])):
                await message.answer(response[0][i])
                await asyncio.sleep(0.5)
            
            await state.set_state(chatStates.mainChat)
            time_answer = datetime.now()
            await rq.set_user_message(user_id, username, True, message.text, response[1], time_message, time_answer)
        elif check_sub_response == False:
            current_date = datetime.now()
            await message.answer('У вас закончилась подписка, приобритите новый тариф.',
                                reply_markup=kb.tarrifs)
            await rq.set_user_log(user_id, 'error-message', 'Subscribe end', current_date)
        else:
            current_date = datetime.now()
            await message.answer('У вас закончились бесплтаные сообщение, пожалуйста приобретите тариф',
                                reply_markup=kb.tarrifs)
            await rq.set_user_log(user_id, 'error-message', 'Free messages end', current_date)
            
   
# --------Chat

# --------Profile

@router.callback_query(lambda callback_query: callback_query.data == 'profile')
async def profile(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    await rq.check_sub(user_id)
    await get_logs(user_id,state, "profileChat", 'btn')

    response = await rq.get_user_sub_info(user_id)
    await state.set_state(chatStates.profileChat)
    if (response == "none"):
        await callback_query.message.answer("У вас нету тарифа, пожалуйста купите тариф или воспользуйтесь другой функцией бота",
                                            reply_markup=kb.main)
        await callback_query.answer()
    else:
        await callback_query.message.answer(f"""Вот инфоормация о состоянии вашего тарифа:
Ваш индефикационный номер: {response[0]}
Ваш тариф: {response[0]}
{response[1]}""", reply_markup=kb.main)
    await callback_query.answer()
    

@router.message(chatStates.profileChat)
async def tariffs_message(message: Message):
    user_id = message.from_user.id
    current_date = datetime.now()
    await message.answer('В этом чате вы не можете писать сообщения! Выберите что то из следующего списка:', 
                         reply_markup=kb.main) 
    await rq.set_user_log(user_id, 'error-message', 'message outside chat', current_date)


# -------Profile

# ------- Mental analysis


@router.callback_query(lambda callback_query: callback_query.data == 'mental_analysis')
async def mental_analysis(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(chatStates.mentalAnalysisChat)
    await callback_query.message.answer("Тут должна быть реализация ментального анализа")
    await callback_query.answer()

@router.message(F.text)
async def mental_message_error(message: Message):
    await message.answer('Вы не можете писать в этом чате, можете перейти ', reply_markup=kb.withoutMentalAnalysis)

# ------- Mental analysis

  

@router.message(F.text)
async def answer_restart_bot(message:Message, state: FSMContext, bot:Bot):
    state_status = await state.get_state()
    if state_status == None:
        await state.set_state(chatStates.mainChat)
        await mainChat_message(message, state, bot)        
        
