import requests
from aiogram import types

from loader import bot, dp
from utils.db.manager_database import Peers, User, db


async def get_config(count, user_id):
    url = f"http://194.87.219.96:8080/data.json"
    responce = requests.get(url)
    result = responce.json()[f'peer{count + 1}']
    await Peers.create(ip=result['ip'], publickey=result['publickey'], user_id=user_id, path=result['address'])
    return 'http://194.87.219.96:8080/data.json'

    
async def check_start(user_id, username):
	data = await User.query.where(User.id==user_id).gino.scalar()
	nickname = 'noname'

	if username is not None:
		nickname = username

	if data is None:
		await User.create(
		id=user_id,
		nickname=nickname
		)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await check_start(
        user_id=message.from_user.id,
        username=message.from_user.username
    )
    await message.answer('hello')


@dp.message_handler(commands='add')
async def start(message: types.Message):
    data = await Peers.select('path').where(Peers.user_id == message.from_user.id).gino.scalar()
    if data is None:
        count = await db.func.count(Peers.publickey).gino.scalar()
        data = await get_config(count, message.from_user.id)

    await bot.send_document(
            document=types.InputFile.from_url(data),
            chat_id=message.chat.id
        )