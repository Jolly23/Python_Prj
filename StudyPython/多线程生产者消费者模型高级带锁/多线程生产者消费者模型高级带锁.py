#!/usr/bin/env python
# coding: utf-8
#copyRight by heibanke

import time
import random
import threading
import os

#当还剩下0个产品时，则不进行消费，待生产者生产
#当生产了 MaxProducts 个产品时，则不进行生产，待消费者消费
MaxProducts = 20

lock = threading.Condition()

#生产者
class Producer(threading.Thread):
    def __init__(self, product,filename):
        self._lock = lock
        self.product = product
        self.file = filename
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if self._lock.acquire():
                if len(self.product) >= MaxProducts:
                    self._lock.wait()
                else:
                    tmp = random.randint(0,10)
                    self.product.append(tmp)
                    print "add    --%d--, size = %d, product = %s" %(tmp,len(self.product),str(self.product))
                    fp=open(self.file,'a')
                    fp.write("add    --%d--, size = %d, product = %s\n" %(tmp,len(self.product),str(self.product)))
                    fp.close()
                self._lock.notify()
                self._lock.release()
            time.sleep(0.1)
            #time.sleep(random.randrange(5))


#消费者
class Consumer(threading.Thread):
    def __init__(self, product, filename):
        self._lock = lock
        self.product = product
        self.file = filename
        threading.Thread.__init__(self)

    def run(self):
        while True:
                if self._lock.acquire():
                    if len(self.product)== 0:
                        self._lock.wait()
                    else:
                        tmp = self.product[0]
                        del self.product[0]
                        print 'consum --%d--, size = %d, product = %s'%(tmp,len(self.product),str(self.product))
                        fp=open(self.file,'a')
                        fp.write('consum --%d--, size = %d, product = %s\n'%(tmp,len(self.product),str(self.product)))
                        fp.close()
                self._lock.notify()
                self._lock.release()
                time.sleep(0.1)
                #time.sleep(random.randrange(4))


if __name__ == '__main__':
    #删除已存在的log.txt文件
    if(os.path.exists('log.txt')):
        os.remove('log.txt')
    product = [] #产品初始化时为0

    for i in range(2):
        p = Producer(product,'log.txt')
        p.start()

    for i in range(1):
        s = Consumer(product,'log.txt')
        s.start()