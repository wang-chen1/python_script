import multiprocessing
import os
import sys
import time

a = 8

def info(title):
    print(title)

    print('module name:', __name__)
    print('moudle info:', sys.modules[__name__])
    print('__main__:', sys.modules['__main__'])
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    print('a:', a)

    print()

def f(name):
    info('function f')
    time.sleep(10)


if __name__ == '__main__':
    a = 9

    info('main line')
    
    mp_module = input("process module (spawn fork forkserver):  ")
    # 如果对创建进程速度要求高且是单线程运行选用 fork
    # 如果多线程情况，避免多线程的 fork 问题选用 forkserver
    # 如果跨平台使用且安全性高使用 spawn
    if mp_module == "spawn":
        # 所有系统都适用
        # 再此线程基础上新建一个子线程。所有模块都是新的
        # bash(361554)───python(368503)─┬─python(368522)
        #                               └─python(368523)
        multiprocessing.set_start_method('spawn')
    elif mp_module == "fork":
        # 仅限于 Linux/unix
        # 再次线程基础上复制一个子线程，所有模块从当前调用的进程中复制。从打印 a 的值可以看出
        # bash(361554)───python(368366)───python(368397)
        # 优：直接从父进程中创建，无需初始化，创建速度快。实现机制相对简单，代码理解和编写都容易
        # 劣：
        multiprocessing.set_start_method('fork')
    elif mp_module == "forkserver":
        # 先创建一个服务器进程，后面所有的需要创建的子进程都从此进程中使用 fork 创建创建。创建出来的服务器进程是单线程的
        # bash(361554)───python(368213)─┬─python(368302)
        #                               └─python(368303)───python(368304)
        multiprocessing.set_start_method('forkserver')
    else:
        raise
    p = multiprocessing.Process(target=f, args=('child',))
    p.start()
    p.join()