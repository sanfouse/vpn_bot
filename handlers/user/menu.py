from configparser import ConfigParser

from aiogram import types
from loader import bot, dp
from utils.db.manager_database import Peers, User, db
import requests
import os


async def get_config(count, user_id):
    config = ConfigParser()
    path = f"http://194.87.219.96:8080/peer{count + 1}/peer{count + 1}.conf"
    responce = requests.get(path)
    open(f'/home/vpn_bot/handlers/user/files/{user_id}.conf', 'wb').write(responce.content)
    config.read(f'/home/vpn_bot/handlers/user/files/{user_id}.conf')
    data_1 = dict(config.items('Interface'))
    data_2 = dict(config.items('Peer'))
    ip = data_1['address']
    publickey = data_2['publickey']
    await Peers.create(ip=ip, publickey=publickey, user_id=user_id, path=path)
    os.remove(f'/home/vpn_bot/handlers/user/files/{user_id}.conf')
    return path

    
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
