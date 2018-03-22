# coding:utf-8

from permission_handler import (
    ManageHandler,
    addRoleHandler,
    delRoleHandler,
    addPermissionHandler,
    delPermissionHandler,
    addMenuHandler,
    delMenuHandler,
    addHandlerHandler,
    delHandlerHandler,
    addUserRoleHandler,
    addRolePermissionHandler,
    delUserRoleHandler,
    addUserDevRoleHandler,
    delUserDevRoleHandler,
)

permission_urls = [
    (r'/permission/manage_list', ManageHandler),  # 用户登录
    (r'/permission/add_role', addRoleHandler),  # 添加角色
    (r'/permission/del_role', delRoleHandler),  # 删除角色
    (r'/permission/add_permission', addPermissionHandler),  # 添加权限
    (r'/permission/del_permission', delPermissionHandler),  # 删除权限
    (r'/permission/add_menu', addMenuHandler),  # 添加菜单权限
    (r'/permission/del_menu', delMenuHandler),  # 删除菜单权限
    (r'/permission/add_handler', addHandlerHandler),  # 添加处理器权限
    (r'/permission/del_handler', delHandlerHandler),  # 删除处理器权限
    (r'/permission/user_add_role', addUserRoleHandler),  # 为用户添加角色
    (r'/permission/role_add_permission', addRolePermissionHandler),  # 为角色添加权限
    (r'/permission/del_user_role', delUserRoleHandler),  # 删除用户权限
    (r'/permission/add_user_dev', addUserDevRoleHandler),  # 为用户添加角色
    (r'/permission/del_user_dev_role', delUserDevRoleHandler),  # 为用户删除角色

]