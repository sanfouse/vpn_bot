from aiogram import types

from loader import dp, bot
from utils.db.manager_database import Peers, User, Servers

    
async def check_start(user_id, username):
	data = await User.query.where(User.user_id==user_id).gino.scalar()
	nickname = 'noname'

	if username is not None:
		nickname = username

	if data is None:
		await User.create(
            user_id=user_id,
            nickname=nickname
		)


async def add_peers():
    servers = await Servers.query.where(Servers.is_parse==False).gino.all()
    if servers is not None:
        for server in servers:
            for peer in range(1, 11):
                await Peers.create(
                    url=f'http://{server.ip_server}:8000/peer{peer}/peer{peer}.conf',
                    server=server.ip_server
                )
                await server.update(is_parse=True).apply()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await check_start(
        user_id=message.from_user.id,
        username=message.from_user.username
    )
    await message.answer('hello')


@dp.message_handler(commands='add')
async def add(message: types.Message):
    await add_peers()
    url = await Peers.select('url').where(Peers.user == message.from_user.id).gino.scalar()
    if url is None:

        peer = await Peers.query.where(Peers.is_free==True).gino.first()
        url = peer.url

        await peer.update(
                is_free=False, 
                user=message.from_user.id
            ).apply()

    await bot.send_document(
            document=types.InputFile.from_url(url),
            chat_id=message.chat.id
        )
