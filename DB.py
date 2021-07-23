import sqlalchemy as sqa

class UserDB():
    def __init__(self):
        self.engine = sqa.create_engine("sqlite:///users.db")
        self.conn = self.engine.connect()
        self.data = sqa.MetaData(self.engine)
        self.User_table = sqa.Table('users', self.data,
                                    sqa.Column('id', sqa.Integer(), primary_key=True),
                                    sqa.Column('name', sqa.String(255), unique=True),
                                    sqa.Column('password', sqa.String(255)),
                                    sqa.Column('image_path',  sqa.String(255), default='PASS')
                                    )
        self.data.create_all(self.engine)

    def insert_user_info(self, user_name, password):
        ins = self.User_table.insert().values(name = user_name,
                                              password = password,
                                              )
        self.conn.execute(ins)

    def insert_user_pic(self, image_path):
        upd = sqa.update(self.User_table).where(self.User_table.c.image_path == 'PASS').values(image_path=image_path)
        self.conn.execute(upd)


    def select_all_data(self):
        select = sqa.select([self.User_table])
        return self.conn.execute(select).fetchall()

    def get_password(self, name):
        select = sqa.select([self.User_table]).where(self.User_table.c.name == name)
        r = self.conn.execute(select)
        return r.fetchone()[2]

    def delete_all(self):
        self.data.drop_all()