# importing utills
from utills import write_excep

#importing library orm system sqlalchemy
from sqlalchemy.orm import sessionmaker

#importing models
from models import Users

#importin utills
from datetime import datetime

# configutation data
from config import engin



class DataBaseORM:

    now = datetime.now()

    def add_user(self, id_user, username, userlogin):
        try:
            new_user = Users(id_user=id_user, username=username, userlogin=userlogin)
            Session = sessionmaker(engin)
            with Session() as s:
                exists_ = s.query(Users).where(Users.id_user == id_user).scalar()
                if exists_:
                    if exists_.is_active == False:
                        exists_.is_active = True
                        s.commit()
                        return 'Вы обнавили подписку'
                    else:
                        return 'Вы и так подписаны'
                s.add(new_user)
                s.commit()
                return  f"Дорогой(ая) {username}, вы успешно подписались на рассылку"
        except Exception as e:
            write_excep(e, 'logfile_db.txt', 'add_user')
            return 'Не удалось подписаться'
    
    def rm_user(self, id_user):
        try:
            Session = sessionmaker(bind=engin)
            with Session() as s:
                exists_ = s.query(Users).filter(Users.id_user == id_user).one()
                if not exists_:
                    return 'Вы и так не подписаны'
                else:
                    s.delete(exists_)
                    s.commit()
                    return f"Дорогой(ая) {exists_.username}, вы успушно удалили свои данные из базы данных"
        except Exception as e:
            write_excep(e, 'logfile_db.txt', 'rm_user')
            return 'Не удалось удалить ваши данные, обратитесь к админу'


    def get_all_active(self): #geting all users data
        try:
            Session = sessionmaker(engin)
            with Session() as s:
                data = s.query(Users).where(Users.is_active == 1)
                return data
        except Exception as e:
            write_excep(e, 'logfile_db.txt', 'get_all')
            return False
    
    def get_user(self, id_user): # function for geting one user
        try:
            Session = sessionmaker(engin)
            with Session() as s:
                user = s.query(Users).where(Users.id_user == id_user).scalar()
                if user:
                    return True, user
                else:
                    return True, 'Такого пользователя не существует'
        except Exception as e:
            write_excep(e, 'logfile_db.txt', 'get_user')
            return False
    
    def update_data(self, obj): # function for update users data
                                # parametr obj is class with three atribets
        try:
            Session = sessionmaker(engin)
            with Session() as s:
                exists_ = s.query(Users).where(Users.id_user == obj.id_user).scalar()
                if exists_:
                    exists_.username = obj.username
                    exists_.userlogin = obj.userlogin
                    s.commit()
                    return True, 'Данные успешно обновлены'
                else:
                    return 'Такого пользователя не существует'
        except Exception as e:
            write_excep(e, 'logfile_db.txt', 'update_data')
            return False
        

    def unsubscribe(self, id_user):
        try:
            Session = sessionmaker(engin)
            with Session() as s:
                exists_ = s.query(Users).where(Users.id_user == id_user).scalar()
                if exists_:
                    exists_.is_active = False
                    s.commit()
                    return 'Успешно отписались'
                else:
                    return 'Вы и так не подписаны на рассылку'
        except Exception as e:
            write_excep(e, 'logfile_db.txt', 'unsubscribe')
            return False
