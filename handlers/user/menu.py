from configparser import ConfigParser

from aiogram import types
from loader import bot, dp
from utils.db.manager_database import Peers, User, db
import requests
import os


async def get_config(count, user_id):
    file_path = f'/files/{user_id}.conf'
    url = f"http://194.87.219.96:8080/peer{count + 1}/peer{count + 1}.conf"
    responce = requests.get(url)
    with open(file_path, 'wb') as file:
        file.write(responce.content)
    config = ConfigParser()
    config.read(file_path)
    interface = dict(config.items('Interface'))
    peer = dict(config.items('Peer'))
    ip = interface['address']
    publickey = peer['publickey']
    await Peers.create(ip=ip, publickey=publickey, user_id=user_id, path=url)
    os.remove(file_path)
    return url

    
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
