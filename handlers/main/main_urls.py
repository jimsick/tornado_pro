# coding:utf-8
from main_handler import MainHandler
from handlers.account.account_urls import accounts_urls
from handlers.permission.permission_urls import permission_urls
from handlers.article.article_urls import article_urls
from handlers.files.files_urls import files_urls
from tornado.web import StaticFileHandler
from handlers.message.message_urls import message_urls
from handlers.account.account_auth_handler import LoginHandler

handlers = [
    (r'/', LoginHandler),
    (r'/images/(.*\.\w{3,5})', StaticFileHandler, {'path': 'files/'}),
]
handlers += accounts_urls
handlers += permission_urls
handlers += article_urls
handlers += files_urls
handlers += message_urls