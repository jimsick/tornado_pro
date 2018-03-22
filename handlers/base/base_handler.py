#coding=utf-8
import tornado.websocket
import tornado.escape
from libs.pycket.session import SessionMixin
from libs.db.dbsession import dbSession
from libs.redis_conn.redis_conn import conn
from models.account.account_user_model import User

users = {
    'user': User
}

class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def initialize(self):  #初始化连接  db为mysql的数据库连接实例  conn为redis的连接实例
        self.db=dbSession
        self.conn=conn
        self.flashes = None

    def get_current_user(self):  #重写方法 如果要使用authenticated方法
        """获取当前用户"""
        username = self.session.get("user_name")
        user = None
        if username:
            user = User.by_name(username)
        return user if user else None
        # if username:
        #     user = users[username['user_tablename']].by_id(username['user_id'])
        #     return user if user else None
        # else:
        #     return None

    def on_finish(self):  #清除连接中的数据
        self.db.close()


class BaseWebSocket(tornado.websocket.WebSocketHandler, SessionMixin):
    def initialize(self):  #初始化连接  db为mysql的数据库连接实例  conn为redis的连接实例
        self.db=dbSession
        self.conn=conn
        self.flashes = None

    def get_current_user(self):  #重写方法 如果要使用authenticated方法
        """获取当前用户"""
        username = self.session.get("user_name")
        user = None
        if username:
            user = User.by_name(username)
        return user if user else None
        # if username:
        #     user = users[username['user_tablename']].by_id(username['user_id'])
        #     return user if user else None
        # else:
        #     return None

    def on_finish(self):  #清除连接中的数据
        self.db.close()
