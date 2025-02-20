import multiprocessing

def sender(queue):
    """向队列中发送数据的进程"""
    messages = ['Hello', 'World', 'Python']
    for message in messages:
        print(f'Sending: {message}')
        queue.put(message)

def receiver(queue):
    """从队列中接收数据的进程"""
    while True:
        message = queue.get()
        if message is None:
            break
        print(f'Received: {message}')

if __name__ == '__main__':
    # 创建一个队列用于进程间通信
    queue = multiprocessing.Queue()

    # 创建发送和接收进程
    sender_process = multiprocessing.Process(target=sender, args=(queue,))
    receiver_process = multiprocessing.Process(target=receiver, args=(queue,))

    # 启动进程
    sender_process.start()
    receiver_process.start()

    # 等待发送进程完成
    sender_process.join()
    # 向队列中发送结束信号
    queue.put(None)
    # 等待接收进程完成
    receiver_process.join()

    print('Communication finished')