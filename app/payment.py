from aiogram.types import LabeledPrice, CallbackQuery, PreCheckoutQuery
from app.keyboards import payment_keyboard

async def send_invoice_handler(callback_query: CallbackQuery, selected_tariff, payment_type):
    stars = 1 if selected_tariff == "Базовый" else 5 if selected_tariff == "Продвинутый" else 10
    rub = 10 if selected_tariff == "Базовый" else 50 if selected_tariff == "Продвинутый" else 100
    amount = 0
    if payment_type == 'stars':
        amount = stars
    else: amount = rub
    prices = [LabeledPrice(label='XTR', amount=amount)]
    await callback_query.message.answer_invoice(
        title='Поддержка канала',
        description=f"Отлично! Вы выбрали {selected_tariff} тариф!",
        prices=prices,
        payload="payment",
        provider_token="",
        currency='XTR',
        reply_markup=payment_keyboard(amount, payment_type)
    )

