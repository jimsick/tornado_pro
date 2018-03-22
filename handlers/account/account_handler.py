# coding=utf-8
from handlers.base.base_handler import BaseHandler
from libs.account.account_libs import (edit_profile,
                                       send_email_libs,
                                       auth_email_libs,
                                       add_avatar_lib
                                       )

class ProfileHandler(BaseHandler):
    """用户信息函数"""
    def get(self):
        self.render('account/account_profile.html', message=None)


class ProfileEditHandler(BaseHandler):
    """编辑用户信息"""
    def get(self):
        self.render('account/account_edit.html')

    def post(self):
        name = self.get_argument('name','')
        password = self.get_argument('password','')
        result = edit_profile(self, name, password)  # 修改用户名和密码
        if result['status'] is False:
            return self.render('account/account_profile.html',message=result['msg'])
        return self.render('account/account_profile.html', message=result['msg'])

class ProfileModifyEmailHandler(BaseHandler):
    """修改邮箱"""
    def get(self):
        self.render('account/account_send_email.html')

    def post(self):
        email = self.get_argument('email','')
        result = send_email_libs(self, email)  # 发送邮件
        if result['status'] is True:
            return self.write(result['msg'])
        return self.write(result['msg'])

class ProfileAuthEmailHandler(BaseHandler):
    """验证验证码修改邮箱"""
    def get(self):
        email_code = self.get_argument('code', '')
        email = self.get_argument('email', '')
        user_id = self.get_argument('user_id', '')
        print email_code, email, user_id

        result = auth_email_libs(self, email, email_code, user_id) # 验证邮箱验证码方法
        if result['status'] is True:
            return self.redirect('/account/user_edit')
        return self.write(result['msg'])

class ProfileAddAvaterHandler(BaseHandler):
    """上传头像"""
    def post(self):
        avatar_data = self.request.files.get('user_avatar')  # input标签的name名
        print avatar_data
        result = add_avatar_lib(self, avatar_data[0]['body'])  #获取上传图片的内容
        if result['status'] is True:
            return self.redirect('/account/user_edit')
        return self.write(result['msg'])


