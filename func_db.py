#importing library orm system sqlalchemy
from sqlalchemy.orm import sessionmaker

#importing models
from models import Users

from config import text_new_user_successfully, text_new_user_invalid, text_repeat_start, engin
import time
import sqlite3


def add_user():
    new_user = Users(id_user=343, username='@adi', userlogin='adi_kg')
    Dbsession = sessionmaker(bind=engin)
    s = Dbsession()
    s.add(new_user)
    s.commit()




class DatabaseInterface:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('users.db')
            self.cur = self.conn.cursor()
            print('sucсessfully connected to database')
        except:
            print('not connected to datebase')


    def create_table(self):
        try:
            exe = self.cur.execute('create table user ( id_user integer unique not null, \
                username varchar, userlogin varchar, sub_time integer, is_active boolean);')
            return True
        except:
            print('happened exeption')
            return False
        finally:
            self.conn.close()

    def add_user(self, id_user, username, userlogin, chat_id):
        try:
            check_user = self.cur.execute(f"select count(id_user) from user where id_user={id_user};")
            n = check_user.fetchone()
            if int(n[0]) > 0:
                self.cur.execute(f"update user set is_active=1 where id_user={id_user}")
                self.conn.commit()
                return True, 'Вы обнавили подписку'
            else:
                d = int(time.time())
                self.cur.execute("INSERT INTO user (id_user, username, userlogin, sub_time, is_active, chat_id) VALUES (?, ?, ?, ?, 1, ?)", (id_user, username, userlogin, d, chat_id))
                self.conn.commit()
                return True, text_new_user_successfully
        except sqlite3.IntegrityError:
            print('Invalid data type') #add logfile and write in that messagen about it string
            return False
        except Exception as e:
            return False, str(e)
        finally:
            self.conn.close()
    
    #funcion for unsubcribtion
    def not_active(self, id_user):
        try:
            exe = self.cur.execute(f"select count(id_user) from user where id_user = {id_user}").fetchone()
            if int(exe[0]) == 0:
                return True, 'You not subscribe'
            else:
                self.cur.execute(f"update user set is_active=0 where id_user = {id_user}")
                self.conn.commit()
                return True, 'You succefully unsubscribe'
        except Exception as e:
            print(f"Happened following exeptions {e}")
            return False
        finally:
            self.conn.close()


    def get_all_id_user(self):
        try:
            exe = self.cur.execute('select id_user from user;')
            id_users = exe.fetchall()
            return id_users, True
        except Exception as e:
            print(f"Happened following except {e}")
            return False
        finally:
            self.conn.close()
    
    def get_chat_id(self):
        try:
            exe = self.cur.execute('select chat_id from user where is_active=1;')
            chat_id = exe.fetchall()
            return chat_id
        except Exception as e:
            (f'Happened following except {e}')
            return False
        finally:
            self.conn.close()