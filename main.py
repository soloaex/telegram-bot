
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import logging
import asyncio

API_TOKEN = 'YOUR_BOT_TOKEN'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Replace with your actual channel usernames
REQUIRED_CHANNELS = ['@earningclubtele', '@earningclubletest', '@soloaex']

# Simulate a database for users
users = {}

async def check_user_channels(user_id):
    for channel in REQUIRED_CHANNELS:
        member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        if member.status not in ['member', 'administrator', 'creator']:
            return False
    return True

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    users.setdefault(user_id, {'referrals': 0, 'referred_by': None})

    text = "👋 Welcome to the Airdrop & Mining Bot!\n\n💸 Join the channels below to get started and unlock various earning opportunities!"
    buttons = [
        [InlineKeyboardButton("📢 Join Earning Club", url='https://t.me/earningclubtele')],
        [InlineKeyboardButton("💬 Join Discussion Group", url='https://t.me/earningclubletest')],
        [InlineKeyboardButton("🌐 Join SoloAEX", url='https://t.me/soloaex')],
        [InlineKeyboardButton("✅ I've Joined", callback_data='verify')]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(text, reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'verify')
async def verify_user(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if await check_user_channels(user_id):
        text = "✅ You're verified! Choose an option below to start earning:"
        buttons = [
            [InlineKeyboardButton("💰 Withdrawable Bots", callback_data='withdrawable')],
            [InlineKeyboardButton("💎 Premium Bots", callback_data='premium')],
            [InlineKeyboardButton("⛏️ Mining Bots", callback_data='mining')]
        ]
    else:
        text = "❌ You haven't joined all required channels. Please join them and click verify again."
        buttons = [[InlineKeyboardButton("🔁 Try Again", callback_data='verify')]]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(user_id, text, reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data in ['withdrawable', 'premium', 'mining'])
async def bot_menu(callback_query: types.CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    user = users.get(user_id, {})

    if data == 'mining' and user.get('referrals', 0) < 5:
        await callback_query.message.answer("⛏️ Mining Bots are locked. Refer 5 friends to unlock.")
        return
    elif data == 'withdrawable':
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("TRX Bot", url="https://t.me/TrxFreeAirdropsBot?start=1342140242")],
            [InlineKeyboardButton("TON Bot", url="https://t.me/TonAirdrop_ibot?start=r03339503340")],
            [InlineKeyboardButton("USDT Bot", url="https://t.me/USDTRewardRobot?start=1342140242")],
            [InlineKeyboardButton("REFI Bot", url="https://t.me/ReficoinvipBot?start=1342140242")],
            [InlineKeyboardButton("DOGE Bot", url="https://t.me/Dogs_droppbot?start=1342140242")],
        ])
        await callback_query.message.answer("🪙 Choose a withdrawable bot:", reply_markup=markup)
    else:
        await callback_query.message.answer(f"{data.capitalize()} bots menu coming soon.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
