# coding=utf-8

import traceback
from models.account.account_user_model import User
from libs.common.send_email.send_email_libs import send_qq_html_email
from datetime import datetime

from random import choice
from string import printable
from uuid import uuid4
import json

def edit_profile(self, name, password):
    """修改用户信息"""
    if password == "":
        return {'status': False, 'msg': "密码不能为空"}

    if name == "":
        return {'status': False, 'msg': "姓名不能为空"}

    user = self.current_user  # 获取当前用户信息
    user.name = name
    user.password = password
    user.update_time = datetime.now()
    self.db.add(user)
    self.db.commit()
    return {'status': True, 'msg': "修改成功"}

def send_email_libs(self, email):
    # 发送邮箱
    email_code = ''.join([choice(printable[:62]) for i in xrange(4)])
    u = str(uuid4())  # 生成uuid
    text_dict = {    # 生成键值对
        u: self.current_user.id,
        'email_code': email_code
    }
    redis_text = json.dumps(text_dict)  # dumps是将dict转化成str格式，loads是将str转化成dict格式。
    content = """
        <p>html邮件格式练习</p>
        <p><a href="http://192.168.169.138:8000/account/auth_email_code?code={}&email={}&user_id={}">邮箱绑定链接</a></p>
    """.format(email_code, email, u)  # 存入邮箱验证码  邮箱 和uuid
    send_fail = send_qq_html_email("877415861@qq.com", [email], "第一课", content)  # 第一课  是标题
    if send_fail:
        return {'status': False, 'msg':'邮箱发送失败'}
    self.conn.setex('email:%s' % email, redis_text, 500)  # 将字符串存入redis中
    return {'status': True, 'msg': '邮箱发送成功'}

def auth_email_libs(self, email, email_code, u):
    """验证邮箱验证码"""
    """
       获取redis中对应的值"email:877415861@qq.com"
       "{"5ec36183-4f12-43f4-81e9-a7ba871d1eb6": 2, "email_code": "FHFx"}" 
    """
    redis_text = self.conn.get('email:%s' % email)

    if redis_text: # 判断如果没有值 则redis过期
        text_dict = json.loads(redis_text)   # dumps是将dict转化成str格式，loads是将str转化成dict格式。
        if text_dict and text_dict['email_code'] == email_code:  # 如果键值对存在 并且 验证码和url中传的值相同
            user = self.current_user
            if not user:  # 可能打开了其他的浏览器  并不存在缓存 所以需要重新进行查询
                user = User.by_id(text_dict[u])
                # dbSession.query(cls).filter_by(id=id).first()  # 如果model内没有用封装类方法 就得这么写

            # print user
            user.email = email
            user.update_time = datetime.now()
            self.db.add(user)
            self.db.commit()
            return {'status': True, 'msg': '邮箱修改成功'}
        return {'status': False, 'msg': '验证码错误'}
    return {'status': False, 'msg': '验证码过期'}


def add_avatar_lib(self, avatar_data):
    """ 上传头像 """
    try:  # 抛出异常
        user = self.current_user
        user.avatar = avatar_data
        user.update_time = datetime.now()
        self.db.add(user)
        self.db.commit()
    except Exception as e:
        print e
        print '------------'
        print traceback.format_exc()
        send_qq_html_email("877415861@qq.com",  # 将报错信息发送到邮箱  或者可以存放在redis中
                           ["877415861@qq.com"],
                           "第一课",
                           traceback.format_exc().replace("\n", '<br>'))
        return {'status': False, 'msg': traceback.format_exc().replace("\n", '<br>')}
    return {'status': True, 'msg': '头像上传成功'}


    # user.avatar(avatar_data)  # 不加装饰器