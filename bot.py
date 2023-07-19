import logging
from config_data.config import load_config
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType

# setup
logging.basicConfig(level=logging.INFO)
config = load_config()
bot = Bot(token=config.tg_bot.BOT_TOKEN)
dp = Dispatcher(bot)

# prices
PRICE_1 = types.LabeledPrice(label="Товар 1", amount=500 * 100)  # 500 RUB


# send invoice
@dp.message_handler(commands=['buy'])
async def payment(message: types.Message):
    PAYMENTS_TOKEN = config.tg_bot.PAYMENTS_TOKEN
    if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await message.answer('Тестовый платеж')
    await bot.send_invoice(message.chat.id,
                           title='Товар 1',
                           description='Описание товара 1',
                           payload="test-invoice-payload",
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           prices=[PRICE_1],
                           photo_url="https://img.freepik.com/premium-vector"
                                     "/pizza-logo-template-suitable-for-rest"
                                     "aurant-and-cafe-logo_607277-267.jpg?w=2000",
                           photo_width=512,
                           photo_height=512,
                           photo_size=512,
                           is_flexible=False,
                           start_parameter="product-1",
                           )


# processing and confirmation of payment before making it
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    total_sum = message.successful_payment.total_amount
    currency = message.successful_payment.currency
    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {total_sum // 100} "
                           f"{currency} прошел успешно!")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
