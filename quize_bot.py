import os
import asyncio
import psycopg2
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_db():
    return psycopg2.connect(DATABASE_URL)

@dp.message(Command("start"))
async def start(message: types.Message):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (user_id BIGINT PRIMARY KEY, points INTEGER DEFAULT 0)")
    cur.execute("INSERT INTO users (user_id) VALUES (%s) ON CONFLICT DO NOTHING", (message.from_user.id,))
    conn.commit()
    cur.close()
    conn.close()
    await message.answer(f"স্বাগতম {message.from_user.first_name}! 🎉\n/quiz দিয়ে খেলো\n/points দিয়ে পয়েন্ট দেখো")

@dp.message(Command("points"))
async def points(message: types.Message):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT points FROM users WHERE user_id = %s", (message.from_user.id,))
    res = cur.fetchone()
    cur.close()
    conn.close()
    await message.answer(f"তোমার পয়েন্ট: {res[0] if res else 0}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
