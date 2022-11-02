"""Seed file to make sample data for employees database"""

from models import User, Post, db
from app import app

db.drop_all()
db.create_all()

u1 = User(user_name='Bunny Boy', first_name='Rocket', last_name='Bondarev', profile_img='https://64.media.tumblr.com/902b77ddf10b9afb2f87ef3212d02705/tumblr_pp8gh2099W1uvq9elo9_1280.jpg')
u2 = User(user_name='Solid Blackheart', first_name='Eleonora', last_name='Bondareva', profile_img='https://scontent-sjc3-1.xx.fbcdn.net/v/t1.6435-9/44324860_10155700134681606_8363376815187689472_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=730e14&_nc_ohc=EnlsIJCTO-sAX8wlJto&_nc_ht=scontent-sjc3-1.xx&oh=00_AfAhn_b_kR52EgFwkp1HBoZi42oyJznKbgWujvaAeAVhNQ&oe=63806E40')
u3 = User(user_name='King Boom Boom', first_name='Max', last_name='Hirtenstein', profile_img='https://scontent-sjc3-1.xx.fbcdn.net/v/t1.6435-9/29387024_3305047302471_775651130649608192_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=730e14&_nc_ohc=oT8DVP6ykz4AX9-r-bg&_nc_ht=scontent-sjc3-1.xx&oh=00_AfBahAMhw189_N3IdsokafbTFJtxA4xCEDYZsETB7gPD3A&oe=63823182')

p1 = Post(post_user='Bunny Boy', title="Where's my dinner?", content="I'm always hungry.")
p2 = Post(post_user='Solid Blackheart', title="I want a nap.", content="I'm always sleepy.")
p3 = Post(post_user='King Boom Boom', title="Where's my new guitar?", content="I ordered it last week!")

db.session.add_all([u1, u2, u3])
db.session.commit()

db.session.add_all([p1, p2, p3])
db.session.commit()

# options to run file:
# ipython: %run seed.py
# python seed.py
