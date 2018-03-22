#coding=utf-8
from uuid import uuid4
from datetime import datetime
from string import printable
from pbkdf2 import PBKDF2

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (create_engine, Column, Integer, String,
                        Text, Boolean, Date, DateTime, ForeignKey)

from libs.db.dbsession import Base
from libs.db.dbsession import dbSession
from models.permission.permisson_model import UserToRole
from models.files.upload_file_model import FilesToUser, DelFilesToUser, Files

class User(Base):
    """用户表"""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))

    name = Column(String(50), nullable=False)
    _password = Column('password', String(64))
    createtime = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime)
    last_login = Column(DateTime)
    loginnum = Column(Integer, default=0)
    _locked = Column(Boolean, default=False, nullable=False)
    _avatar = Column(String(64))
    email = Column(String(50))
    mobile = Column(String(50))

    # 建立orm查询关系,与用户表和消息表的关系
    #user_message = relationship("Message", secondary=Flike.__table__)
    articles = relationship("Article", backref="user")

    comments = relationship("Comment", backref="user")

    second_comments = relationship("SecondComment", backref="user")
    
    roles = relationship("Role", secondary=UserToRole.__table__)  # 根据用户查询该用户所有角色

    users_files = relationship('Files', secondary=FilesToUser.__table__, lazy='dynamic')
    users_files_del = relationship('Files', secondary=DelFilesToUser.__table__, lazy='dynamic')


    @classmethod
    def all(cls):
        return dbSession.query(cls).all()

    @classmethod
    def by_id(cls, id):
        return dbSession.query(cls).filter_by(id=id).first()

    @classmethod
    def by_uuid(cls, uuid):
        return dbSession.query(cls).filter_by(uuid=uuid).first()

    @classmethod
    def by_name(cls, name):
        return dbSession.query(cls).filter_by(name=name).first()

    def _hash_password(self, password):
        return PBKDF2.crypt(password, iterations=0x2537)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        print self._hash_password(password)
        self._password = self._hash_password(password)

    def auth_password(self, other_password):
        if self._password is not None:
            return self.password == PBKDF2.crypt(other_password, self.password)
        else:
            return False

    @property
    def avatar(self):  # 获取真实字段
        return self._avatar if self._avatar else "default_avatar.jpeg"


    @avatar.setter
    def avatar(self, image_data):   # 赋值
        class ValidationError(Exception):  # 异常类
            def __init__(self, message):
                super(ValidationError, self).__init__(message)
        if 64 < len(image_data) < 1024 * 1024:  # 判断图片大小
            import imghdr
            import os
            ext = imghdr.what("", h=image_data)  # 返回值为图片扩展名
            print ext
            print self.uuid
            if ext in ['png', 'jpeg', 'gif', 'bmp'] and not self.is_xss_image(image_data): #如果前16个字符都可打印的话说明可能不是图片文件
                if self._avatar and os.path.exists("static/images/useravatars/" + self._avatar):  # 如果文件存在
                    os.unlink("static/images/useravatars/" + self._avatar)  # 删除文件
                file_path = str("static/images/useravatars/" + self.uuid + '.' + ext)  # 重新获取文件路径  uuid.扩展名
                with open(file_path, 'wb') as f:
                    f.write(image_data)  # 写入文件
                self._avatar = self.uuid + '.' + ext  # uuid.扩展名
            else:
                raise ValidationError("not in ['png', 'jpeg', 'gif', 'bmp']")
        else:
            raise ValidationError("64 < len(image_data) < 1024 * 1024 bytes")

    def is_xss_image(self, data):  # 打印前16个字符
        return all([char in printable for char in data[:16]])

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        assert isinstance(value, bool)
        self._locked = value

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'last_login': self.last_login,
        }
