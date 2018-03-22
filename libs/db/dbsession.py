#coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# 连接数据库的数据
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'tornado_pro'
USERNAME = 'zyb'
PASSWORD = '931121'
# DB_URI的格式：dialect（mysql/sqlite）+driver://username:password@host:port/database?charset=utf8
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,
                                                              PASSWORD,
                                                              HOSTNAME,
                                                              PORT,
                                                              DATABASE
                                                              )


# 1创建一个engine引擎
engine = create_engine(DB_URI, echo=False )
# 2sessionmaker生成一个session类
Session = sessionmaker(bind=engine)
# 3创建一个session实例
dbSession = Session()
# 4创建一个模型基类
Base = declarative_base(engine)



