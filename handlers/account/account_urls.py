# coding:utf-8

from account_auth_handler import LoginHandler, CaptchaHandler, RegistHandler, MobileCodeHandler
from account_handler import (ProfileHandler,
                             ProfileEditHandler,
                             ProfileModifyEmailHandler,
                             ProfileAuthEmailHandler,
                             ProfileAddAvaterHandler)

accounts_urls = [
    (r'/auth/user_login', LoginHandler),  # 用户登录
    (r'/auth/captcha', CaptchaHandler),  # 图形验证码
    (r'/auth/user_regist', RegistHandler),  # 用户注册
    (r'/auth/mobile_code', MobileCodeHandler),  # 短信验证码
    (r'/account/user_profile', ProfileHandler),  # 用户中心
    (r'/account/user_edit', ProfileEditHandler),  # 用户修改
    (r'/account/send_user_email', ProfileModifyEmailHandler),  # 发送邮件
    (r'/account/auth_email_code', ProfileAuthEmailHandler),  # 邮箱验证
    (r'/account/avatar', ProfileAddAvaterHandler),  # 上传头像
]