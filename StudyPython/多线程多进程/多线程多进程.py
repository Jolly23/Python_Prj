#!/usr/bin/python
# coding=utf-8


import time
from multiprocessing import Process
from threading import Thread

def countdownNum(n):
    while(n > 0):
        n -= 1

COUNT = 100000000

def thread_process_job(n,Thread_Process,job):
    '''
    :param n:多线程或多进程数
    :param Thread_Process:  Thread/Process类
    :param job: 需要执行的函数任务
    '''
    local_time = time.time()
    #实例化多线程或多进程
    thread_or_processes = [Thread_Process(target=job, args=(COUNT//n,)) for i in xrange(n)]
    for t in thread_or_processes:
        t.start()
    for t in thread_or_processes:
        t.join()

    print n,Thread_Process.__name__,u'需要 ',time.time()-local_time


if __name__ == '__main__':
    print u'线程'
    for i in [1,2,4,8]:
        thread_process_job(i,Thread,countdownNum)

    print u'进程'
    for i in [1,2,4,8]:
        thread_process_job(i,Process,countdownNum)
