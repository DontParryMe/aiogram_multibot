import asyncio
import csv
import logging
import sys
from aiogram import Bot, Dispatcher, types


tokens = set()

with open('tokens.csv', 'r', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        tokens.add(row[0])


dispatchers = {token: Dispatcher() for token in tokens}
bots = {token: Bot(token) for token in tokens}

for token, dispatcher in dispatchers.items():
    bot = bots[token]

    @dispatcher.message()
    async def echo_handler(message: types.Message, bot:Bot=bot):
        await bot.send_message(message.chat.id, f"Вы написали: {message.text}")


async def main():
    tasks = []
    for token, dispatcher in dispatchers.items():
        tasks.append(dispatcher.start_polling(bots[token]))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
