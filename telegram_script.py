
import asyncio
import telegram


async def send_telegram_message(chat_id, message_text):
    bot = telegram.Bot(token='6287170813:AAEcQCTsxorctXYQVRSJ2ES5KkN0MjolnVY')
    await bot.send_message(chat_id=chat_id, text=message_text)


async def main():
    # Отправка тестового сообщения
    bot = telegram.Bot(token='6287170813:AAEcQCTsxorctXYQVRSJ2ES5KkN0MjolnVY')
    await bot.send_message(chat_id='@store_materasso', text='Test message')

    # Получение последнего обновления и chat_id
    updates = await bot.get_updates()
    last_update = updates[-1]
    chat_id = last_update.message.chat_id
    print(f"Chat ID: {chat_id}")

    # Отправка сообщения с использованием полученного chat_id
    message_text = "Привет, мир!"
    await send_telegram_message(chat_id, message_text)


if __name__ == '__main__':
    asyncio.run(main())
