#coding=utf-8

from celery_test_module.celery_tasks import add,manage_redis

# celery -A celery_test_module worker -l info -c 5
# celery -A celery_test_module worker -l info -c 5 -B  每次自动运行
# 可开启多个celery分布式执行


# add.delay(5, 7)
# manage_redis()

import time
for i in xrange(50):
    add.delay(i+1, 0)
    time.sleep(1)