# coding=utf-8
from models.permission.permisson_model import Role, Permission, Menu, Handler
from models.account.account_user_model import User
from libs.flash.flash_lib import flash


def permission_manager_list_lib(self):
    """01权限管理页面函数"""
    roles = Role.all()
    permissions = Permission.all()
    menus = Menu.all()
    handlers = Handler.all()
    users = User.all()

    # 研发员工
    dev_role = Role.by_name('研发员工')
    dev_users = dev_role.users if dev_role else []
    dev_roleid = dev_role.id if dev_role else ''
    return roles, permissions, menus, handlers, users, dev_users, dev_roleid


def add_role_lib(self, name):
    """02添加角色"""
    try:
        role = Role.by_name(name)
        if role is not None:
            flash(self, '角色已存在', 'error')
        role = Role()
        role.name = name
        self.db.add(role)
        self.db.commit()
        flash(self, '角色添加成功', 'success')
        # return {'status': True, 'msg': '角色添加成功'}
    except Exception as e:
        print e
        flash(self, '角色添加失败', 'error')
        # return {'status': False, 'msg': '角色添加失败'}


def del_role_lib(self, roleid):
    """03删除角色"""
    try:
        role = Role.by_id(roleid)
        if role is None:
            flash(self, '角色不存在', 'error')
        self.db.delete(role)  # 删除
        self.db.commit()
        flash(self, '角色删除成功', 'success')
    except Exception as e:
        print e
        flash(self, '角色删除失败', 'error')


def add_permission_lib(self, name, strcode):
    """04添加权限"""
    try:
        permission = Permission.by_name(name)
        if permission is not None:
            flash(self, '权限添加失败', 'error')
        permission = Permission()
        permission.name = name
        permission.strcode = strcode
        self.db.add(permission)
        self.db.commit()
        flash(self, '权限添加成功', 'success')
    except Exception as e:
        print e
        flash(self, '权限添加失败', 'error')


def del_permission_lib(self, permissionid):
    """05删除权限"""
    try:
        permission = Permission.by_id(permissionid)
        if permission is None:
            flash(self, '权限不存在', 'error')
        self.db.delete(permission)
        self.db.commit()
        flash(self, '权限已删除', 'success')
    except Exception as e:
        print e
        flash(self, '权限删除失败', 'error')



def add_menu_lib(self, name, permissionid):
    """06菜单添加权限"""
    try:
        permission = Permission.by_id(permissionid)
        menu = Menu.by_name(name)
        if permission is None:
            flash(self, '权限已存在', 'error')
        if menu is None:
            menu = Menu()  # 不存在创建menu
        menu.name = name
        menu.permission = permission
        self.db.add(menu)
        self.db.commit()
        flash(self, '菜单权限添加成功', 'success')
    except Exception as e:
        print e
        flash(self, '菜单权限添加失败', 'error')


def del_menu_lib(self, menuid):
    """07菜单删除权限"""
    try:
        menu = Menu.by_id(menuid)
        if menu is None:
            flash(self, '菜单不存在', 'error')
        self.db.delete(menu)
        self.db.commit()
        flash(self, '菜单权限删除成功', 'success')
    except Exception as e:
        print e
        flash(self, '菜单权限删除失败', 'error')


def add_handler_lib(self, name, permissionid):
    """08处理器添加权限"""
    try:
        permission = Permission.by_id(permissionid)
        handler = Handler.by_name(name)
        if permission is None:
            flash(self, '权限不存在', 'error')
        if handler is None:
            handler = Handler()  # 不存在创建Handler
        handler.name = name
        handler.permission = permission
        self.db.add(handler)
        self.db.commit()
        flash(self, '处理器权限添加成功', 'success')
    except Exception as e:
        print e
        flash(self, '处理器权限添加失败', 'error')


def del_handler_lib(self, handlerid):
    """09处理器删除权限"""
    try:
        handler = Handler.by_id(handlerid)
        if handler is None:
            flash(self, '处理器不存在', 'error')
        self.db.delete(handler)
        self.db.commit()
        flash(self, '处理器权限删除成功', 'success')
    except Exception as e:
        print e
        flash(self, '处理器权限删除失败', 'error')


def add_user_role_lib(self, userid, roleid):
    """10用户添加角色"""
    try:
        user = User.by_id(userid)
        role = Role.by_id(roleid)
        if user is None or role is None:
            flash(self, '用户或者角色不存在', 'error')
        user.roles.append(role)  # 添加到中间表
        self.db.add(user)
        self.db.commit()
        flash(self, '用户添加角色成功', 'success')
    except Exception as e:
        print e
        flash(self, '用户添加角色失败', 'error')


def add_permission_role_lib(self, permissionid, roleid):
    """11给角色添加权限"""
    try:
        permission = Permission.by_id(permissionid)
        role = Role.by_id(roleid)
        if permission is None or role is None:
            flash(self, '权限或者角色不存在', 'error')
        role.permissions.append(permission)  # 添加到中间表
        self.db.add(role)
        self.db.commit()
        flash(self, '处理器权限删除失败', 'success')
    except Exception as e:
        print e
        flash(self, '角色添加权限失败', 'error')


def del_user_role_lib(self, userid):
    """12删除用户角色"""
    try:
        user = User.by_id(userid)
        if user is None:
            flash(self, '用户不存在', 'error')
        # []
        user.roles = []
        # user.roles.remove(obj)  # 删除一个对象
        # user.roles.pop()  # 弹出最后一个
        self.db.add(user)
        self.db.commit()
        flash(self, '用户删除角色成功', 'success')
    except Exception as e:
        print e
        flash(self, '用户删除角色失败', 'error')

def add_user_dev_role_lib(self, userid, roleid):
    """13为用户添加角色"""
    try:
        user = User.by_id(userid)
        role = Role.by_id(roleid)
        if user is None or role is None:
            flash(self, '用户或者角色不存在', 'error')
        user.roles.append(role)  # 添加到中间表
        self.db.add(user)
        self.db.commit()
        flash(self, '用户添加角色成功', 'success')
    except Exception as e:
        print e
        flash(self, '用户添加角色失败', 'error')


def del_user_dev_role_lib(self, userid, roleid):
    """14为用户删除角色"""
    try:
        user = User.by_id(userid)
        role = Role.by_id(roleid)
        if user is None or role is None:
            flash(self, '用户或者角色不存在', 'error')
        user.roles.remove(role)  # 添加到中间表
        self.db.add(user)
        self.db.commit()
        flash(self, '用户删除角色成功', 'success')
    except Exception as e:
        print e
        flash(self, '用户删除角色失败', 'error')
