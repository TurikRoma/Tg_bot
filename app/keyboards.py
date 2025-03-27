from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder  

main = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Переход в чат', callback_data='go_chat')],
                                             [InlineKeyboardButton(text='Приобрести подписку', callback_data='tariffs')],
                                             [InlineKeyboardButton(text='Профиль', callback_data='profile')],
                                             [InlineKeyboardButton(text='Ментальный анализ', callback_data='mental_analysis')]])

withoutTariffs = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Переход в чат', callback_data='go_chat')],
                                             [InlineKeyboardButton(text='Профиль', callback_data='profile')],
                                             [InlineKeyboardButton(text='Ментальный анализ', callback_data='mental_analysis')]
                                             ])

withoutMentalAnalysis = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Переход в чат', callback_data='go_chat')],
                                             [InlineKeyboardButton(text='Приобрести подписку', callback_data='tariffs')],
                                             [InlineKeyboardButton(text='Профиль', callback_data='profile')],
                                             ])


get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер', request_contact=True)]],
                                 resize_keyboard=True)

tarrifs = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Приобрести подписку', callback_data='tariffs')]])

registration = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Регистрация', callback_data='registration')],
                                             ])

sex = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Мужской', callback_data='sex_man')],
                                             [InlineKeyboardButton(text='Женский', callback_data='sex_women')],
                                             ])

skip = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Пропустить', callback_data='skip')],
                                             ])

name_bot = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Пропустить', callback_data='skip_name_bot')],
                                             ])
mental_analysis_choise = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Хочу попробовать', callback_data='try_mental_analysis')],
                                                               [InlineKeyboardButton(text='Нет, вернуться в чат с Бадди', callback_data='back_to_bot')],
                                             ])
mental_analysis_condition = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Болтать с Бадди', callback_data='back_to_bot')],
                                                               [InlineKeyboardButton(text='Уже готово!', callback_data='start_mental_analysis')],
                                             ])

back_to_bot = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Болтать с Бадди', callback_data='back_to_bot')],
                                             ])

tech_sup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Тех. поддержка', url='https://t.me/buddyk_support')],
                                             ])





def create_tarif_keyboard(selected_tariff):
    tariffs = ["Базовый", "Продвинутый", "Smart"]
    buttons = []
    for i in range(0, len(tariffs),2):
        row = [InlineKeyboardButton(text=f"{tariff} {'✅' if tariff == selected_tariff else ' '}", 
                callback_data=f'select_{tariff}') 
                for tariff in tariffs[i:i+2]]
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text = 'Выбрать', callback_data='choose_tariff')])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
 

def create_payment_type_keybord(selected_tariff):
    stars = 1 if selected_tariff == "Базовый" else 5 if selected_tariff == "Продвинутый" else 10
    rub = 10 if selected_tariff == "Базовый" else 50 if selected_tariff == "Продвинутый" else 100
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=f'{stars} ⭐️', callback_data='payment_stars'),
                                                  InlineKeyboardButton(text=f'{rub} $', callback_data='payment_rub')],
                                                 ])

def payment_keyboard(amount, payment_type):
    builder = InlineKeyboardBuilder()
    if payment_type == "stars":
        builder.button(text=f'Оплатить {amount} ⭐️', pay=True)
    else:
        builder.button(text=f'Оплатить {amount} $', pay=True)

    return builder.as_markup()