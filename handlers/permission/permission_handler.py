# coding=utf-8
from libs.permission.permission_auth.permission_interface_libs import handler_permission
from handlers.base.base_handler import BaseHandler
from libs.permission.permission_lib import (
    permission_manager_list_lib,
    add_role_lib,
    del_role_lib,
    add_permission_lib,
    del_permission_lib,
    add_menu_lib,
    del_menu_lib,
    add_handler_lib,
    del_handler_lib,
    add_user_role_lib,
    add_permission_role_lib,
    del_user_role_lib,
    add_user_dev_role_lib,
    del_user_dev_role_lib,
)


class ManageHandler(BaseHandler):
    def get(self):
        # self.write("aaa")
        roles, permissions, menus, handlers, users, dev_users, dev_roleid = permission_manager_list_lib(self)
        kw = {
            'roles': roles,
            'permissions': permissions,
            'menus': menus,
            'handlers': handlers,
            'users': users,
            'dev_users': dev_users,
            'dev_roleid': dev_roleid,
        }

        self.render("permission/permission_list.html", **kw)


class addRoleHandler(BaseHandler):
    """02添加角色"""
    @handler_permission('AddRoleHandler', 'handler')
    def post(self):
        name = self.get_argument('name', '')
        result = add_role_lib(self, name)
        self.redirect('/permission/manage_list')


class delRoleHandler(BaseHandler):
    """03删除角色"""
    # @handler_permission('DelRoleHandler', 'handler')
    def get(self):
        roleid = self.get_argument('id', '')
        result = del_role_lib(self, roleid)
        self.redirect('/permission/manage_list')


class addPermissionHandler(BaseHandler):
    """04添加权限"""
    def post(self):
        name = self.get_argument('name', '')
        strcode = self.get_argument('strcode', '')
        result = add_permission_lib(self, name, strcode)
        self.redirect('/permission/manage_list')


class delPermissionHandler(BaseHandler):
    """05删除权限"""
    def get(self):
        permissionid = self.get_argument('id', '')
        result = del_permission_lib(self, permissionid)
        self.redirect('/permission/manage_list')


class addMenuHandler(BaseHandler):
    """06添加菜单权限"""
    def post(self):
        name = self.get_argument('name', '')
        permissionid = self.get_argument('permissionid', '')
        result = add_menu_lib(self, name, permissionid)
        self.redirect('/permission/manage_list')


class delMenuHandler(BaseHandler):
    """07删除菜单权限"""
    def get(self):
        menuid = self.get_argument('menuid', '')
        result = del_menu_lib(self, menuid)
        self.redirect('/permission/manage_list')


class addHandlerHandler(BaseHandler):
    """08添加处理器权限"""
    def post(self):
        name = self.get_argument('name', '')
        permissionid = self.get_argument('permissionid', '')
        result = add_handler_lib(self, name, permissionid)
        self.redirect('/permission/manage_list')


class delHandlerHandler(BaseHandler):
    """09删除处理器权限"""
    def get(self):
        handlerid = self.get_argument('handlerid', '')
        result = del_handler_lib(self, handlerid)
        self.redirect('/permission/manage_list')


class addUserRoleHandler(BaseHandler):
    """10用户添加角色"""
    def post(self):
        userid = self.get_argument('userid', '')
        roleid = self.get_argument('roleid', '')
        result = add_user_role_lib(self, userid, roleid)
        self.redirect('/permission/manage_list')


class addRolePermissionHandler(BaseHandler):
    """11给角色添加权限"""
    def post(self):
        permissionid = self.get_argument('permissionid', '')
        roleid = self.get_argument('roleid', '')
        result = add_permission_role_lib(self, permissionid, roleid)
        self.redirect('/permission/manage_list')


class delUserRoleHandler(BaseHandler):
    """12删除用户权限"""
    def get(self):
        userid = self.get_argument('userid', '')
        result = del_user_role_lib(self, userid)
        self.redirect('/permission/manage_list')


class addUserDevRoleHandler(BaseHandler):
    """13为用户添加角色"""
    def post(self):
        userid = self.get_argument('userid', '')
        roleid = self.get_argument('roleid', '')
        result = add_user_dev_role_lib(self, userid, roleid)
        self.redirect('/permission/manage_list')


class delUserDevRoleHandler(BaseHandler):
    """14为用户删除角色"""
    @handler_permission('DelUserDevRoleHandler', 'handler')
    def get(self):
        userid = self.get_argument('userid', '')
        roleid = self.get_argument('roleid', '')
        result = del_user_dev_role_lib(self, userid, roleid)
        self.redirect('/permission/manage_list')