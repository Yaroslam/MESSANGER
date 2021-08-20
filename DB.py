import sqlalchemy as sqa
from CONST import DB_PATH
import sqlite3
import os

class UserDB():
    def __init__(self):
        self.engine = sqa.create_engine("sqlite:///" + DB_PATH + "/users.db", connect_args = {'check_same_thread': False})
        self.conn = self.engine.connect()
        self.data = sqa.MetaData(self.engine)
        self.User_table = sqa.Table('users', self.data,
                                    sqa.Column('id', sqa.Integer(), primary_key=True),
                                    sqa.Column('name', sqa.String(255), unique=True),
                                    sqa.Column('password', sqa.String(255)),
                                    sqa.Column('image_path', sqa.String(255), default='PASS'),
                                    sqa.Column('ip', sqa.String(255), default='PASS')
                                    )
        self.data.create_all(self.engine)

    def insert_user_info(self, user_name, password):
        ins = self.User_table.insert().values(name=user_name,
                                              password=password,
                                              )
        self.conn.execute(ins)

    def insert_user_pic(self, image_path):
        upd = sqa.update(self.User_table).where(self.User_table.c.image_path == 'PASS').values(image_path=image_path)
        self.conn.execute(upd)

    def insert_user_IP(self, ip):
        upd = sqa.update(self.User_table).where(self.User_table.c.ip == 'PASS').values(ip=ip)
        self.conn.execute(upd)

    def select_all_data(self):
        select = sqa.select([self.User_table])
        return self.conn.execute(select).fetchall()

    def get_password(self, name):
        select = sqa.select([self.User_table]).where(self.User_table.c.name == name)
        r = self.conn.execute(select)
        return r.fetchone()[2]

    def get_id(self, name):
        select = sqa.select([self.User_table]).where(self.User_table.c.name == name)
        r = self.conn.execute(select)
        k = r.fetchone()
        return k[0]

    def get_ip_by_id(self, id):
        select = sqa.select([self.User_table]).where(self.User_table.c.id == id)
        r = self.conn.execute(select)
        return r.fetchone()[4]

    def get_users_by_key(self, key_word):
        looking_for = '%{0}%'.format(key_word)
        select = sqa.select(self.User_table).where(self.User_table.c.name.like(looking_for))
        return self.conn.execute(select).fetchall()

    def get_pic(self, name):
        select = sqa.select([self.User_table]).where(self.User_table.c.name == name)
        r = self.conn.execute(select)
        return r.fetchone()[3]

    def get_pic_by_id(self, id):
        select = sqa.select([self.User_table]).where(self.User_table.c.id == id)
        r = self.conn.execute(select)
        return r.fetchone()[3]

    def delete_all(self):
        self.data.drop_all()


class MesagesDB():
    def __init__(self, from_id, to_id):
        self.engine = sqa.create_engine(f"sqlite:///{DB_PATH}/{from_id}to{to_id}.db",connect_args = {'check_same_thread': False})
        self.conn = self.engine.connect()
        self.data = sqa.MetaData(self.engine)
        self.messages_table = sqa.Table(f'{from_id}to{to_id}', self.data,
                                        sqa.Column('id', sqa.Integer(), primary_key=True),
                                        sqa.Column('from_id', sqa.Integer()),
                                        sqa.Column('message', sqa.String(255)),
                                        )
        self.data.create_all(self.engine)

    def get_last(self):
        pass


    def insetr_message(self, message, from_id):
        ins = self.messages_table.insert().values(from_id=from_id,
                                                  message=message
                                                  )
        self.conn.execute(ins)

    def get_last_message(self):
        select = sqa.select([self.messages_table])
        id = self.conn.execute(select).rowcount()
        selection = sqa.select(self.messages_table).where(self.messages_table.c.id.like(id))
        r = self.conn.execute(selection)
        return r.fetchone()

    def select_all_masseges(self):
        select = sqa.select([self.messages_table])
        return self.conn.execute(select).fetchall()