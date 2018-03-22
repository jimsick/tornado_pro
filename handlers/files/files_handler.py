# coding=utf8

from handlers.base.base_handler import BaseHandler
from libs.files.files_lib import (
    files_list_lib,
    upload_files_lib,
    files_message_lib,
    file_page_lib,
    del_files_lib,
    del_final_files_lib,
    recovery_files_lib,
    files_download_lib,
    upload_qiniu_files_lib,
    files_download_qiniu_lib,
    create_sharing_links_lib,
    get_username_lib,
    get_sharing_files_lib,
    files_sharing_list_lib,
    save_sharing_files_lib
)



"""文件列表显示"""
class FilesListHandler(BaseHandler):
    def get(self, page):
        pagination = files_list_lib(self, page)
        kw = {'pagination': pagination}
        self.render('files/files_list.html', **kw)

"""文件上传"""
class FilesUploadHandler(BaseHandler):
    def get(self):
        self.render('files/files_upload.html')

    def post(self):
        upload_files =self.request.files.get('importfile', None)
        result = upload_files_lib(self, upload_files)
        if result is None:
            return self.write({'status': 400, 'msg': '有错误了'})
        return self.write({'status': 200, 'msg': '有错误了', 'data': result})
        # [{'body': '', 'content_type': u'text/plain', 'filename': u'111.txt'}]
        # upload_files['body']
        # upload_files['content_type']
        # upload_files['filename']
        print upload_files


"""查询文件"""
class FilesMessageHandler(BaseHandler):
    def get(self):
        uuid = self.get_argument('uuid', '')
        files = files_message_lib(self, uuid)
        kw = {'files': files}
        self.render('files/files_message.html', **kw)


"""文章分页列表"""
class FilesPageListHandler(BaseHandler):
    def get(self, page):
        files_page,files_page_del = file_page_lib(self, page)
        kw = {
            'files': files_page['split_content'],
            'files_page': files_page,
            'files_del': files_page_del,
            # 'files_page_del': files_page_del,
        }
        self.render('files/files_page_list.html', **kw)

# -----------------------------分享链接处理器-------------------------------
class FilesCreateSharingLinks(BaseHandler):
    """001创建分享链接"""

    def get(self):
        uuid = self.get_argument('uuid', '')
        fileslinks, password = create_sharing_links_lib(self, uuid)
        kw = {'fileslinks': fileslinks, 'password': password}
        self.render('files/files_create_sharing_links.html', **kw)

class FilesAuthSharingLinks(BaseHandler):
    """002使用密码验证分享链接"""

    def get(self):
        uu = self.get_argument('uuid', '')
        result = get_username_lib(self, uu)
        if result['status'] is False:
            kw = {'username': result['username'], 'uuid1': uu, 'msg': result['msg']}
            return self.render('files/files_auth_sharing_links.html', **kw)
        kw = {'username': result['username'], 'uuid1': uu, 'msg': ''}
        self.render('files/files_auth_sharing_links.html', **kw)

    def post(self):
        uu = self.get_argument('uuid', '')
        password = self.get_argument('password', '')
        result = get_sharing_files_lib(self, uu, password)
        if result['status'] is False:
            return self.write({'status': 400, 'msg': result['msg']})
        return self.write({'status': 200, 'msg': result['msg'], 'links': result['links']})

class FilesSharingListHandler(BaseHandler):
    """003查看分享的文件"""

    def get(self):
        uu = self.get_argument('uuid', '')
        print self.session.set('sharing', 'aa')
        result = files_sharing_list_lib(self, uu)
        if result['status'] is True:
            kw = {'files': result['data'], 'uuid': result['uuid']}
            return self.render('files/files_sharing_list.html', **kw)
        return self.write(result['msg'])

class FilesSaveSharingHandler(BaseHandler):
    """004保存分享的文件"""

    def get(self):
        uu = self.get_argument('uuid', '')
        result = save_sharing_files_lib(self, uu)
        if result['status'] is True:
            return self.redirect('/files/files_page_list/1')
        return self.write(result['msg'])

        # -----------------------------分享链接处理器-------------------------------


#-----------------------------回收站接口-----------------------------

"""删除文件到回收站"""
class DelFilesHandler(BaseHandler):
    def get(self):
        uuid = self.get_argument("uuid", None)
        del_files_lib(self, uuid)
        return self.redirect("/files/files_page_list/1")

class FinalDelFilesHandler(BaseHandler):
    """002最终删除"""

    def get(self):
        uuid = self.get_argument('uuid', '')
        del_final_files_lib(self, uuid)
        return self.redirect('/files/files_page_list/1')

class RecoveryFilesHandler(BaseHandler):
    """003从回收站恢复"""

    def get(self):
        uuid = self.get_argument('uuid', '')
        recovery_files_lib(self, uuid)
        return self.redirect('/files/files_page_list/1')
#-----------------------------回收站接口结束-----------------------------

""" 文档下载"""
import time
class FilesDownloadsHandler(BaseHandler):
    def get(self):
        uuid = self.get_argument("uuid", "")
        if uuid != '':
            filepath = 'files/%s' % uuid
            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header('Content-Disposition', 'attachment; filename=%s' % uuid)
            with open(filepath, 'rb') as f:
                while 1:
                    data = f.read(1024*5)
                    if not data:
                        break
                    self.write(data)
                    self.flush()
                    time.sleep(1)
            self.finish()
        else:
            self.write('no uuid')

import tornado.gen  # 协程装饰器
from concurrent.futures import ThreadPoolExecutor  # 线程池
executor1 = ThreadPoolExecutor(50)  # 线程人数   进程和核数有关
class FilesDownloadsHandler(BaseHandler):
    executor = executor1
    @tornado.gen.coroutine
    def get(self):
        uuid = self.get_argument("uuid", "")
        if uuid != '':
            yield files_download_lib(self, uuid)  # IO操作使用线程 ， 计算密集型操作使用进程 。硬盘取出数据发送到客户端是IO操作
        else:
            self.write('no uuid')



#-----------------------------七牛上传下载-----------------------------
"""文件上传"""
class FilesUploadQiniuHandler(BaseHandler):
    def get(self):
        self.render('files/files_upload.html')

    def post(self):
        upload_files =self.request.files.get('importfile', None)
        result = upload_qiniu_files_lib(self, upload_files)
        if result is None:
            return self.write({'status': 400, 'msg': '有错误了'})
        return self.write({'status': 200, 'msg': '有错误了', 'data': result})
        # [{'body': '', 'content_type': u'text/plain', 'filename': u'111.txt'}]
        # upload_files['body']
        # upload_files['content_type']
        # upload_files['filename']
        print upload_files

"""文件下载"""
class FilesDownLoadQiniuHandler(BaseHandler):
    def get(self):
        uuid = self.get_argument('uuid', '')
        result = files_download_qiniu_lib(self, uuid)
        if result['status'] is True:
            return self.redirect(result['data'])
        else:
            return self.write(result['msg'])