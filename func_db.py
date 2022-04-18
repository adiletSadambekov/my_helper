from config import text_new_user_successfully, text_new_user_invalid, text_repeat_start
import time
import sqlite3


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

    def add_user(self, id_user, username, userlogin, is_active, chat_id):
        try:
            check_user = self.cur.execute(f"select count(id_user) from user where id_user={id_user};")
            n = check_user.fetchone()
            if int(n[0]) > 0:
                return True, text_repeat_start
            else:
                d = int(time.time())
                self.cur.execute("INSERT INTO user (id_user, username, userlogin, sub_time, is_active, chat_id) VALUES (?, ?, ?, ?, ?, ?)", (id_user, username, userlogin, d, is_active, chat_id))
                self.conn.commit()
                return True, text_new_user_successfully
        except sqlite3.IntegrityError:
            print('Invalid data type') #add logfile and write in that messagen about it string
            return False
        except:
            print('an unknown error has occurred')
            return False, text_new_user_invalid
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
            exe = self.cur.execute('select chat_id from user;')
            chat_id = exe.fetchall()
            return chat_id
        except Exception as e:
            (f'Happened following except {e}')
            return False
        finally:
            self.conn.close()