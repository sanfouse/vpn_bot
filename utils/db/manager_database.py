import asyncio

from gino import Gino
from utils.config import DATABASE_URL

db = Gino()

print(DATABASE_URL)
class User(db.Model):

  __tablename__ = 'users'

  id = db.Column(db.BigInteger(), primary_key=True)
  nickname = db.Column(db.Unicode(), default='noname')


class Peers(db.Model):

  __tablename__ = 'peers'

  ip = db.Column(db.Unicode(), default='0.0.0.0')
  user_id = db.Column(db.BigInteger(), primary_key=True, nullable=True, default=None)
  publickey = db.Column(db.Unicode())
  path = db.Column(db.Unicode())

async def main():
  await db.set_bind(
    DATABASE_URL
  )
  print('[*] >> DATABASE CONNECTED')
  await db.gino.create_all()


asyncio.get_event_loop().run_until_complete(main())