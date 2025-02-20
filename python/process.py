import multiprocessing
import time

def worker(num):
    """进程要执行的任务"""
    print(f'Worker {num} started')
    result = num * num
    time.sleep(10)
    print(f'Worker {num} result: {result}')
    print(f'Worker {num} finished')
    print(time.asctime())

if __name__ == '__main__':
    processes = []
    for i in range(5):
        # 创建进程对象
        p = multiprocessing.Process(target=worker, args=(i,))
        processes.append(p)
        # 启动进程
        p.start()

    # 等待所有进程执行完毕
    for p in processes:
        p.join()

    print('All workers finished')
