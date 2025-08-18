'''
Telegram-bot for neuro-finance
'''
import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from ..ai import ChoaAI
from ..avatar import Avatar

load_dotenv()
choa = ChoaAI()
avatar = Avatar()

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")


# All handlers should be attached to the Router (or Dispatcher) 
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    '''
    This handler receives messages with `/start` command
    '''
    await message.answer(f'Hello, {html.bold(message.from_user.full_name)}! \nМеня зовут 초아. Нажмите /help, чтобы узнать больше о моих способностях.')


@dp.message(Command('help'))
async def cmd_help(message: Message) -> None:
    '''
    This handler receives messages with `/help` command
    '''
    await message.answer('Список команд: \n/help - список команд;\n/about - обо мне и моих задачах;\n/journal - предоставление журнала операции.')


@dp.message(Command('about'))
async def cmd_about(message: Message) -> None:
    '''
    This handler receives messages with `/about` command
    '''
    await message.answer('Я нейро-финансист в торговой компании. В мои обязанности входит ведение журнала операции для ОДДС. А также написание аналитических записок по просьбам руководства')


@dp.message(Command('journal'))
async def cmd_journal(message: Message) -> None:
    '''
    This handler receives messages with `/journal` command
    '''
    await message.answer('journal of operation.csv')


@dp.message()
async def text(message: Message) -> None:
    '''
    This handler receives messages with text
    '''
    response = await choa.neuro_finansist(message.from_user.id, message.text)

    if response['module'] == 'analyze':
        video_file = await avatar.create_video(response['text'])
        await message.bot.send_video(chat_id=message.chat.id, video=video_file)
    else:
        await message.answer(response['text'])


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())