'''
python的多任务编程可以通过多进程，多线程来实现

多任务的概念：同一时间同时执行多个任务

多任务的两种表现形式：
并发：在一段时间内交替去执行多个任务
并行：在一段时间内真正的同时一起执行多个任务

进程：资源分配的最小单位。一个正在运行的程序至少有一个进程。
线程：程序执行的最小单位。一个进程中最少有一个线程来执行程序。例如一个微信（进程）打开两个聊天窗口（线程）

'''

'''
导入线程模块
1 import threading

2 通过线程类创建线程对象
线程对象 = threading.Thread(target=任务名)

3 启动线程执行任务
线程对象.start()
'''

'''
线程的特点：

1 主线程会等所有的子线程执行结束后再结束

2 要想主线程不等待子线程执行完成可以设置守护主线程
work_thread.setDaemon(True)
work_thread.start()

3 线程之间执行是无序的

4 获取当前的线程信息
cur_thread = threading.current_thread()
print(cur_thread)
'''

import time
import threading

def sing(num):
    for i in range(num):
        print('唱歌...')
        time.sleep(0.5)

def dance(num):
    for i in range(num):
        print('跳舞...')
        time.sleep(0.5)

#使用thread在jupyter中可以正常print
sing_thread = threading.Thread(target=sing, args=(3, ))
dance_thread = threading.Thread(target=dance, kwargs={'num':3})

sing_thread.start()
dance_thread.start()

# 多线程读取文件
def copy_file(file_name, source_dir, dest_dir):
    '''
    source_path: 源文件路径
    dest_path: 目标文件路径
    '''
    source_path = source_dir + '/' + file_name
    dest_path = dest_dir + '/' + file_name
    
    with open(source_path, 'rb') as source_file:
        with open(dest_path, 'wb') as dest_file:
            while True:
                data = source_file.read(1024)
                if data:
                    dest_file.write(data)
                else:
                    break

file_list = os.listdir(source_dir)

for file_name in file_list:
    #使用多进程实现多任务拷贝
    sub_thread = threading.Thread(target=copy_file, args=(file_name, source_dir, dest_dir))
    sub_thread.start()
    
import threading
import time

def func():
    print('T1 start')
    for i in range(10):
        time.sleep(0.1)
    print('T1 finish')
    
t1_thread = threading.Thread(target=func, name='T1')
t1_thread.start()
'''
使用join命令目的：多线程是同时进行的线程任务。如果想等所有线程结束再开始新的任务，那么可以使用.join()来作为分隔。
为了all_done在最后输出。
要不然会先输出all_done，再输出T1 finish
！！！！ 注意，多进程程中也有join命令。使用方式和多线程中的相同。

'''
t1_thread.join()
print('all done')

from queue import Queue
'''
因为使用多线程时是没有return功能的，因此使用queue来收集数据
'''
def func(l, q):
    for i in range(len(l)):
        l[i] = l[i]**2
    q.put(l) #把l列表的结果放到q里面

def multi_threading(data):
    q = Queue()
    threads = []
    results = []
    
    #开始线程运算
    for i in range(4):
        t = threading.Thread(target=func, args=(data[i], q))
        t.start()
        #收集所有的子线程
        threads.append(t)
        
    #把每一个子线程附加到主线程
    for thread in threads:
        thread.join()
    
    for i in range(4):
        results.append(q.get()) #从q中按顺序依次拿出一个值
        
    return results

data = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 2, 4]]
#把四批数据分别放入四个线程中
multi_threading(data)


# 使用lock锁来规避同一个变量在多个线程中由于运算的无序性带来的影响
'''
以下的程序通过lock.acquire()和lock.release()的配合，对于A会先执行job1中的运算，再执行job2中的运算。
'''
def job1():
    global A, lock
    lock.acquire()
    for i in range(5):
        A += 1
        print('job1',A)
    lock.release()
    
def job2():
    global A, lock
    lock.acquire()
    for i in range(5):
        A += 10
        print('job2',A)
    lock.release()
    
lock = threading.Lock()
A = 0
t1 = threading.Thread(target=job1)
t2 = threading.Thread(target=job2)
t1.start()
t2.start()
