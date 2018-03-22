# coding:utf-8

"""
文件说明:
    登录页面所有跳转以及方法处理

"""
from handlers.base.base_handler import BaseHandler
from libs.account.account_auth_libs import (create_captcha_img,
                                            auth_captche,
                                            login,
                                            get_mobile_code_lib,
                                            regist)



class CaptchaHandler(BaseHandler):
    """生成验证码"""
    def get(self):
        pre_code = self.get_argument('pre_code','')  # 上一次请求的时间戳
        code = self.get_argument('code','')  # 本次请求的时间戳
        img = create_captcha_img(self,pre_code,code)  # 获取验证码
        self.set_header("Content-Type","image/jpg")  # 设置头
        self.write(img)  # 输出验证码

class LoginHandler(BaseHandler):
    """登录"""
    def get(self):
        self.render("account/auth_login.html")

    def post(self):
        name = self.get_argument('name', '')
        password = self.get_argument('password', '')
        code = self.get_argument('code', '')
        captcha_code = self.get_argument('captcha', '')
        result = auth_captche(self, captcha_code, code)
        if result['status'] is False:
            return self.write({'status':400, 'msg': result['msg']})
        result = login(self, name, password)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})

        return self.write({'status':400, 'msg': result['msg']})


class MobileCodeHandler(BaseHandler):
    """03发送手机短信"""
    def post(self):
        mobile = self.get_argument('mobile', '')
        code = self.get_argument('code', '')
        # captcha = self.get_argument('captcha', '')
        # print mobile, code, captcha
        # result = get_mobile_code_lib(self, mobile, code, captcha)
        result = get_mobile_code_lib(self, mobile, code)

        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})


class RegistHandler(BaseHandler):
    """04注册函数"""
    def get(self):
        self.render("account/auth_regist.html", message="用户注册")

    def post(self):
        mobile = self.get_argument('mobile','')
        mobile_captcha = self.get_argument('mobile_captcha','')
        name = self.get_argument('name','')
        code = self.get_argument('code','')
        password1 = self.get_argument('password1','')
        password2 = self.get_argument('password2','')
        captcha = self.get_argument('captcha','')
        result = regist(self, name, mobile, mobile_captcha, password1, password2, captcha, code)
        if result['status'] is True:
            # return self.write({'status': 200, 'msg': result['msg']})
            self.redirect('/auth/user_login')
            # return self.render('auth/user_login', message=result['msg'])
        else:
            self.redirect('/auth/user_regist')


