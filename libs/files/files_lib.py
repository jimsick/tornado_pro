# coding:utf8
from models.files.upload_file_model import Files,DelFilesToUser
from uuid import uuid4
from datetime import datetime
from libs.pagination.pagination_libs import Pagination
from libs.flash.flash_lib import flash
from tornado.concurrent import run_on_executor
from libs.qiniu.qiniu_libs import upload_qiniu_file_content, down_qiniu_file
import json
from string import printable
from random import randint, choice


def files_list_lib(self, page):
    page = int(page)
    items = self.db.query(Files).limit(MAX_PAGE).offset((page - 1) * MAX_PAGE).all()
    if page == 1 and len(items) < MAX_PAGE:
        total = len(items)
    else:
        total = self.db.query(Files).order_by(None).count()
    return Pagination(page, MAX_PAGE, total, items)



def upload_files_lib(self, upload_files):
    """总体文件上传"""
    # [{'body': '', 'content_type': u'text/plain', 'filename': u'111.txt'}]
    # upload_files['body']
    # upload_files['content_type']
    # upload_files['filename']
    img_path_list = []
    for upload_file in upload_files:
        file_path = save_file(self, upload_file)
        img_path_list.append(file_path)
    return img_path_list if img_path_list else None

def save_file(self, upload_file):
    """保存单个文件"""
    files_ext = upload_file['filename'].split('.')[-1]
    files_type = ['jpg', 'bmp', 'png', 'mp4', 'ogg', 'mp3', 'txt']
    if files_ext not in files_type:
        return {'status': False, 'msg': '文件格式不正确', 'data': ''}
    uuidname = str(uuid4())+ '.%s' % files_ext
    file_content = upload_file['body']
    old_file = Files.file_is_existed(file_content)
    if old_file is not None:
        file_path = 'http://192.168.169.138:8000/images?uuid=' + old_file.uuid
        file_id = Files.by_uuid(old_file.uuid).id  # 老文件的uuid
        # 连表查询  查询删除的表中是否有老文件的id
        isExist = self.db.query(Files.id, DelFilesToUser.files_id).join(DelFilesToUser).filter_by(files_id=file_id).first()
        # 如果存在则从回收站中恢复
        if isExist != None:
            files = Files.by_uuid(old_file.uuid)
            files.files_users_del.remove(self.current_user)
            files.files_users.append(self.current_user)
            self.db.add(files)
            self.db.commit()
        return {'status': True, 'msg': '文件上传成功（硬盘中存在文件）', 'data': file_path}

    url = 'files/' + uuidname
    with open(url, 'wb') as f:
        f.write(file_content)
    file_name = upload_file['filename']
    files = Files()
    files.uuid = uuidname
    files.filename = file_name
    files.content_length = len(file_content)
    files.content_type = upload_file['content_type']
    files.updata_time = datetime.now()
    files.file_hash = upload_file['body']
    files.files_users.append(self.current_user)
    files.user_id = self.current_user.id
    self.db.add(files)
    self.db.commit()
    file_path = 'http://192.168.169.138:8000/images/' + files.uuid
    return {'status': True, 'msg': '文件上传成功', 'data': file_path}


def files_message_lib(self, uuid):
    """查询文件uuid"""
    return Files.by_uuid(uuid)

MAX_PAGE = 5
def file_page_lib(self, page):
    """文章分页"""
    files = self.current_user.users_files
    files_page_del = self.current_user.users_files_del
    files_page = get_page_list(int(page), files, MAX_PAGE)
    return files_page, files_page_del

def get_page_list(current_page, content, MAX_PAGE):
    """文章分页算法"""
    start = (current_page - 1) * MAX_PAGE  # 2-1 *2  算出起始位置下标
    end = start + MAX_PAGE  # 2 + 2
    split_content = content[start: end]  # 切片
    total = content.count()
    count = total/MAX_PAGE  # 8/2=4  算出总页数
    if total % MAX_PAGE != 0:  # 如果有9也就要+1页
        count += 1
    pre_page = current_page - 1  # 上一页
    next_page = current_page + 1  # 下一页
    if pre_page == 0:
        pre_page = 1
    if pre_page == 0:
        next_page = count
    # 第一种情况 总页数小于5 ，显示的总页数 +1
    if count < 5:
        pages = [p for p in xrange(1, count+1)]  #
    # 第二种情况 现点击的页数小于等于3  ，page(页数)显示1到5
    elif current_page <= 3:
        pages = [p for p in xrange(1, 6)]  # 2   1,2,3,4,5
    # 第三种情况 现点击数比总页数-2 大， 那么页数就显示 最后5页
    elif current_page >= count - 2:  #
        pages = [p for p in xrange(count - 4, count + 1)]  # 9   6,7,8,9,10
    # 第四种情况   点击的页数  离最大页数超过2  离最小页数也超过2
    else:
        pages = [p for p in xrange(current_page - 2, current_page + 3)]  # 15    13,14,15,16,17
    return {
        'split_content': split_content,
        'count': count,
        'pre_page': pre_page,
        'next_page': next_page,
        'pages': pages,
        'current_page': current_page,
    }


def del_files_lib(self, uuid):
    """删除文章到回收站"""
    try:
        files = Files.by_uuid(uuid)
        files.files_users.remove(self.current_user)
        files.files_users_del.append(self.current_user)
        self.db.add(files)
        self.db.commit()
    except Exception as e:
        print e

def del_final_files_lib(self, uuid):
    """彻底删除文件"""
    try:
        files = Files.by_uuid(uuid)
        files.files_users_del.remove(self.current_user)
        self.db.add(files)
        self.db.commit()
    except Exception as e:
        print e

def recovery_files_lib(self, uuid):
    """恢复文件"""
    try:
        files = Files.by_uuid(uuid)
        files.files_users_del.remove(self.current_user)
        files.files_users.append(self.current_user)
        self.db.add(files)
        self.db.commit()
    except Exception as e:
        print e


import time
@run_on_executor
def files_download_lib(self, uuid):
        filepath = 'files/%s' % uuid
        filename = Files.by_uuid(uuid).filename
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=%s' % filename)
        with open(filepath, 'rb') as f:
            while 1:
                data = f.read(1024 * 5)
                if not data:
                    break
                self.write(data)
                self.flush()
                time.sleep(1)
        self.finish()


# ---------------------------上传文件到七牛--------------------
def upload_qiniu_files_lib(self, upload_files):
    """总体文件上传"""
    # [{'body': '', 'content_type': u'text/plain', 'filename': u'111.txt'}]
    # upload_files['body']
    # upload_files['content_type']
    # upload_files['filename']
    img_path_list = []
    for upload_file in upload_files:
        file_path = save_qiniu_file(self, upload_file)
        img_path_list.append(file_path)
    return img_path_list if img_path_list else None

def save_qiniu_file(self, upload_file):
    """保存单个文件"""
    files_ext = upload_file['filename'].split('.')[-1]
    files_type = ['jpg', 'bmp', 'png', 'mp4', 'ogg', 'mp3', 'txt']
    if files_ext not in files_type:
        return {'status': False, 'msg': '文件格式不正确', 'data': ''}

    files_content = upload_file['body']
    old_file = Files.file_is_existed(files_content)
    if old_file is not None:
        file_path = 'http://192.168.169.138:8000/images?uuid=' + old_file.uuid  # 这里要改成七牛云的链接
        file_id = Files.by_uuid(old_file.uuid).id  # 老文件的uuid
        # 连表查询  查询删除的表中是否有老文件的id
        isExist = self.db.query(Files.id, DelFilesToUser.files_id).join(DelFilesToUser).filter_by(files_id=file_id).first()
        # 如果存在则从回收站中恢复
        if isExist != None:
            files = Files.by_uuid(old_file.uuid)
            files.files_users_del.remove(self.current_user)
            files.files_users.append(self.current_user)
            self.db.add(files)
            self.db.commit()
        return {'status': True, 'msg': '文件上传成功（硬盘中存在文件）', 'data': file_path}

    ret, info = upload_qiniu_file_content(files_content)
    print ret
    print info
    if info.status_code != 200:
        return {'status': False, 'msg': '文件上传到七牛失败', 'data': ''}

    file_name = upload_file['filename']
    files = Files()
    files.uuid = ret  # 保存的七牛返回的文件名
    files.filename = file_name
    files.content_length = len(files_content)
    files.content_type = upload_file['content_type']
    files.updata_time = datetime.now()
    files.file_hash = upload_file['body']
    files.files_users.append(self.current_user)
    files.user_id = self.current_user.id
    self.db.add(files)
    self.db.commit()
    file_path = 'http://192.168.169.138:8000/images/' + files.uuid  # 这里要改成七牛云的链接
    return {'status': True, 'msg': '文件上传到七牛成功', 'data': file_path}


"""文件下载"""
def files_download_qiniu_lib(self, uuid):
    if uuid == '':
        return {'status': False, 'msg': '没有文件ID'}
    old_file = Files.by_uuid(uuid)
    if old_file is None:
        return {'status': False, 'msg': '文件不存在'}
    qiniu_url = 'http://192.168.169.138:8000/images?uuid=%s' % uuid  # 这里要改成七牛云的链接
    url = down_qiniu_file(qiniu_url)
    print url
    return {'status': True, 'data': url}


#-----------------------------分享链接处理器--(可以用另一个用户登录后分享文件)-----------------------------
def create_sharing_links_lib(self, file_uuid):
    """001创建分享链接"""
    #生成redis键
    uu = str(uuid4())
    #生成4位提取密码
    password = ''.join([choice(printable[:62]) for i in xrange(4)])
    #创建字典
    redis_dict = {
        'user': self.current_user.name,
        'file_uuid': file_uuid,
        'password': password
    }
    #序列化字典
    reids_json = json.dumps(redis_dict)
    #保存到redis中
    self.conn.setex('sharing_links:%s' % uu, reids_json, 300)
    return 'http://192.168.169.138:8000/files/files_auth_sharing_links?uuid=%s'%uu, password


def get_username_lib(self,uu):
    """001获取分享者姓名"""
    #查询redis
    redis_json = self.conn.get('sharing_links:%s' % uu)
    #如果没有返回过期
    if redis_json is None:
        return {'status':False, 'msg':'分享已经过期', 'username':''}
    #如果有反序列化，返回用户名
    redis_dict = json.loads(redis_json)
    return {'status':True, 'msg':'', 'username': redis_dict['user']}



def get_sharing_files_lib(self, uu, password):
    """002使用密码验证分享链接"""
    # 查询redis
    redis_json = self.conn.get('sharing_links:%s' % uu)
    # 如果没有返回已经过期
    if redis_json is None:
        return {'status':False, 'msg':'分享已经过期', 'username':''}
    # 如果有反序列化
    redis_dict = json.loads(redis_json)
    #对比用户提交的密码与redis保存的密码
    if password == redis_dict['password']:
        #对比成功，密码保存当前用户的session
        self.session.set('sharing_links_password', password)
        #返回分享链接
        links = '/files/files_sharing_list?uuid=%s' % uu
        return {'status': True, 'msg': '分享11111成功', 'links': links, 'username':''}
    return {'status':False, 'msg': '分享密码输入错误', 'username': redis_dict['user']}


def files_sharing_list_lib(self, uu):
    """003查看分享的文件"""
    if uu == '':
        return {'status': False, 'msg': 'uuid不存在', 'data': ''}
    #获取当前用户的提取密码
    password = self.session.get('sharing_links_password')
    if not password:
        #如果没有密码重新获取链接
        return {'status': False, 'msg': '请重新获取链接', 'data': ''}
    # 查询redis
    redis_json = self.conn.get('sharing_links:%s' % uu)
    # 如果没有返回已经过期，并删除session
    if redis_json is None:
        del self.session['sharing_links_password']
        return {'status': False, 'msg': '分享已经过期', 'data': ''}
    # 如果有反序列化
    redis_dict = json.loads(redis_json)
    # 对比用户session中保存的密码和redis保存的密码
    if password != redis_dict['password']:
        # 如果不相等提示错误
        return {'status': False, 'msg': '您没有获得这个文件的链接', 'data': ''}
    # 返回文件
    files = Files.by_uuid(redis_dict['file_uuid'])
    return {'status': True, 'msg': '分享成功', 'data': [files], 'uuid':uu}


def save_sharing_files_lib(self, uu):
    """004保存分享的文件"""
    if uu == '':
        return {'status': False, 'msg': 'uuid不存在', 'data': ''}
    # 获取当前用户的提取密码
    password = self.session.get('sharing_links_password')
    if not password:
        # 如果没有密码重新获取链接
        return {'status': False, 'msg': '没有权限', 'data': ''}
    # 查询redis
    redis_json = self.conn.get('sharing_links:%s' % uu)
    # 如果没有返回已经过期，并删除session
    if redis_json is None:
        del self.session['sharing_links_password']
        return {'status': False, 'msg': '分享已经过期', 'data': ''}
    # 如果有反序列化
    redis_dict = json.loads(redis_json)
    # 对比用户session中保存的密码和redis保存的密码
    if password != redis_dict['password']:
        # 如果不相等提示错误
        return {'status': False, 'msg': '您没有获得这个文件的链接', 'data': ''}
    # 把文件保存到当前用户
    files = Files.by_uuid(redis_dict['file_uuid'])
    files.files_users.append(self.current_user)
    self.db.add(files)
    self.db.commit()
    return {'status': True, 'msg': '保存成功', 'data': ''}


#-----------------------------分享链接处理器结束-------------------------------
