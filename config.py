#coding=utf-8
from libs.flash.flash_lib import get_flashed_messages
from libs.permission.permission_auth.permission_interface_libs import menu_permission
settings = dict(
        template_path='templates',  # 设置模板路径
        static_path='static',  # 设置静态文件路径
        debug=True,  # 调试模式
        cookie_secret='aaaa',  # cookie加密方式
        login_url='/auth/user_login',  #a uth  指定默认的路径
        xsrf_cookies=True,  # 防止跨域攻击
        ui_methods={  # 使用uimethod
            "menu_permission": menu_permission,
            "get_flashed_messages": get_flashed_messages,
        },
        #pycket配置信息
        pycket={
            'engine': 'redis',
            'storage': {
                'host': 'localhost',
                'port': 6379,
                'db_sessions': 5,
                'db_notifications': 11,
                'max_connections': 2 ** 31,
            },
            'cookies': {
                'expires_days':30, #设置过期时间
                #'max_age':5000,
            }
        }
)