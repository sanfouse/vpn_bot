import asyncio

from gino import Gino
from utils.config import DATABASE_URL

db = Gino()

class User(db.Model):

  __tablename__ = 'users'

  user_id = db.Column(db.BigInteger(), primary_key=True)
  nickname = db.Column(db.Unicode(), default='noname')


class Servers(db.Model):

  __tablename__ = 'servers'

  ip_server = db.Column(db.Unicode(), primary_key=True)
  is_parse = db.Column(db.Boolean, unique=False, default=False)


class Peers(db.Model):

  __tablename__ = 'peers'

  url = db.Column(db.Unicode())
  is_free = db.Column(db.Boolean, default=True)
  user = db.Column(db.ForeignKey('users.user_id'), default=None, nullable=True, primary_key=True)
  server = db.Column(db.ForeignKey('servers.ip_server'))


async def main():
  await db.set_bind(
    DATABASE_URL
  )
  print('[*] >> DATABASE CONNECTED')
  await db.gino.create_all()


asyncio.get_event_loop().run_until_complete(main())
