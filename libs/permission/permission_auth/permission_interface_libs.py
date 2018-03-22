#coding=utf-8
import functools
from models.permission.permisson_model import Handler, Menu
from libs.flash.flash_lib import flash
obj_model = {
    "handler": Handler,
    "menu": Menu,
}

class PermissionAuth(object):
    def __init__(self):
        self.user_permission = set()
        self.obj_permission = ''

    def permission_auth(self, user, name, types, model):
        # 获取当前用户权限
        roles = user.roles

        for role in roles:
            for permission in role.permissions:
                self.user_permission.add(permission.strcode)

        # 获取handler的权限
        handler = model[types].by_name(name)

        if handler is None:
            return
        permission = handler.permission
        self.obj_permission = permission.strcode
        # 如果handler对应的权限存在用户的所有权限集合中，返回true
        print '-'*50
        print self.user_permission
        print '-' * 50
        print self.obj_permission
        if self.obj_permission in self.user_permission:
            return True
        return False


# 装饰器
def handler_permission(handlername, types):
    """

        :param handlername:
        :param types:
        :return:
        例：
            @handler_permission('DelPermissionHandler', 'handler')

    """
    def func(method):
        @functools.wraps(method)  # 标配  只有好处没坏处
        def wrapper(self, *args, **kwargs):
            if PermissionAuth().permission_auth(self.current_user, handlername, types, obj_model):  # 为真表示有权限
                return method(self, *args, **kwargs)
            else:
                # flash(self, '没有删除角色的权限', 'error')
                # self.redirect('/permission/manage_list')
                self.write("没有删除角色的权限")
        return wrapper
    return func

# 菜单权限
def menu_permission(self, menuname, types):
    if PermissionAuth().permission_auth(self.current_user, menuname, types, obj_model):  # 为真表示有权限
        return True
    else:
        return False