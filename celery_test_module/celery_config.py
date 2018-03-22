#coding=utf-8
from __future__ import absolute_import
from datetime import timedelta
from celery.schedules import crontab

BROKER_URL = 'redis://127.0.0.1/2'  # 消息代理
CELERY_RESULT_BACKEND = 'redis://127.0.0.1/3'  # 消息返回结果

CELERT_TIMEZONE='ASIA/Shanghai'
CELERYBEAT_SCHEDULE = {
    # 按秒执行
    'redis_manage':{
        'task': 'celery_test_module.celery_tasks.manage_redis',
        'schedule': timedelta(seconds=5)
    },
    # 每个小时的第39分钟执行
    'redis_manage':{
        'task': 'celery_test_module.celery_tasks.manage_redis',
        'schedule': crontab(minute=39)
    }
}