'''
python的多任务编程可以通过多进程，多线程来实现

多任务的概念：同一时间同时执行多个任务

多任务的两种表现形式：
并发：在一段时间内交替去执行多个任务
并行：在一段时间内真正的同时一起执行多个任务

进程：资源分配的最小单位。一个正在运行的程序至少有一个进程。
线程：程序执行的最小单位。一个进程中最少有一个线程来执行程序。例如一个微信（进程）打开两个聊天窗口（线程）

进程和线程的对比：

1 关系对比 
线程是依附在进程里面的，没有进程就没有线程
一个进程默认提供一条线程，进程可以创建多个线程

2 区别对比
创建进程的开销要大于创建线程的开销
进程是操作系统资源分配的基本单位，线程是CPU调度的基本单位
线程不能独立执行，必须依存在进程中

3 优缺点对比
进程优缺点：可以使用多核，资源开销大
线程优缺点：资源开销小，不能使用多核

！！建议有资源的情况下使用多进程。速度快。使用多进程还有可能比不上普通的代码速度。
'''

'''
进程的特点：

1 主进程会等待所有的子进程执行结束再结束

2 设置守护主进程: 主进程退出后子进程直接销毁，不再执行子进程中的代码
work_process.daemon = True
work_process.start()

'''

'''
1导入进程包
import multiprocessing

2通过进程类创建进程对象
进程对象 = multiprocessing.Process(target=任务名) 任务名指的就是函数名

3启动进程执行任务
进程对象.start()
'''
#普通代码
import time

def sing():
    for i in range(3):
        print('唱歌...')
        time.sleep(0.5)

def dance():
    for i in range(3):
        print('跳舞...')
        time.sleep(0.5)
        
sing()
dance()

# 以上运行部分可改写为：
# 实践发现 在 jupyter使用多进程时，无法使用print打印
sing_process = multiprocessing.Process(target=sing)
dance_process = multiprocessing.Process(target=dance)

sing_process.start()
dance_process.start()

#使用多进程执行包含参数的函数
'''
当程序中的进程数量越来越多时，如果没有办法区分主进程和子进程，那么就无法有效地进行进程管理。其实每个进程都是有编号的。

获取进程编号的两种方式：

1 获取当前进程编号
os.getpid()

2 获取当前父进程编号
os.getppid()

'''
import time

def sing(num):
    print('唱歌进程的编号：', os.getpid())
    print('唱歌进程的父进程编号：', os.getppid())
    for i in range(num):
        print('唱歌...')
        time.sleep(0.5)

def dance(num):
    print('跳舞进程的编号：', os.getpid())
    print('跳舞进程的父进程编号：', os.getppid())
    for i in range(num):
        print('跳舞...')
        time.sleep(0.5)

print('主进程的编号：', os.getpid())
sing_process = multiprocessing.Process(target=sing, args=(3,)) #逗号不能省略
dance_process = multiprocessing.Process(target=dance, kwargs={'num':3}) #传递参数的另外一种形式

sing_process.start()
dance_process.start()

# 多进程读取文件
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
    sub_process = multiprocessing.Process(target=copy_file, args=(file_name, source_dir, dest_dir))
    sub_process.start()
    
# 进程池 pool ：把所有要运行的东西放到池子里，python自己解决分配和运算问题。
# 相当于使用pool可以正常使用return,有返回值
# 在jupyter运行以下代码，运行超时。。
import multiprocessing as mp

def job(a):
    return a*a

def multicore(lst):
    pool = mp.Pool()
    res = pool.map(job, lst)
    print(res)

lst = [1, 2, 3, 4, 5]
multicore(lst)

import multiprocessing as mp
#和多线程一样，多进程也需要使用lock来保证同一变量的处理顺序。
def job(num):
    global v, lock
    lock.acquire()
    for i in range(5):
        time.sleep(0.1)
        v += num
        print(v)
    lock.release()
        
lock = mp.Lock()
v = 0

p1 = mp.Process(target=job, args=(1,))
p2 = mp.Process(target=job, args=(10,))
p1.start()
p2.start()
p1.join()
p2.join()
