import hashlib

from sqlalchemy import Column, String, Text

import config
import secret
from models.base_model import SQLMixin, db


class User(SQLMixin, db.Model):
    __tablename__ = 'User'
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    image = Column(String(100), nullable=False, default='/images/3.jpg')
    email = Column(String(50), nullable=False, default=config.test_mail)

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        salted = hashlib.sha256((password + salt).encode('ascii')).hexdigest()
        return salted

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        print('register', form)
        if len(name) > 2 and User.one(username=name) is None:
            # 错误，只应该 commit 一次
            # u = User.new(form)
            # u.password = u.salted_password(pwd)
            # User.session.add(u)
            # User.session.commit()
            form['password'] = User.salted_password(form['password'])
            u = User.new(form)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        query = dict(
            username=form['username'],
            password=User.salted_password(form['password']),
        )
        print('validate_login', form, query)
        return User.one(**query)

    @classmethod
    def confirm_password(cls, form, user):
        password = form.get('old_pass', '')
        print('confirm_pswd', form)
        u = User.one(id=user.id,password=password)
        if u is not None:
            u = User.update(id=user.id, password=User.salted_password(form['new_pass']))
            return u
        else:
            return None

    @classmethod
    def confirm_username(cls, form):
        username = form.get('name', '')
        print('confirm_username', form)
        u = User.one(username=username)
        if u is not None:
            u = User.update(username=form['value'])
            return u
        else:
            return None

    @staticmethod
    def guest():
        u = User()
        u.username = '游客'
        return u