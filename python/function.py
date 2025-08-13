class FileHandler:

    def __init__(self, file_name, mode):
        self.file_name = file_name
        self.mode = mode
        self.file = None

    def __enter__(self):
        # 打开文件并返回文件对象
        self.file = open(self.file_name, self.mode)
        return self.file

    # exc_type, exc_val, exc_tb,这三个是调用 exit 时自动传入的参数
    # 没有发生异常时三个值都为 None，
    def __exit__(self, exc_type, exc_val, exc_tb):
        # 关闭文件
        if self.file:
            self.file.close()

class DataBase:

    def __init__(self, id, address):
        self.id = id
        self.address = address
    # 用来获取 key 的值
    def __getitem__(self, key):
        return self.__dict__.get(key, "100")



def enter():
    # __enter__ 上下文协议的重要组成部分，主管资源分配、文件的打开和关闭等
    # with 会先调用 enter 后调用 exit
    with FileHandler("../test.txt", 'tw') as f:
        f.write("tsetsest")


def getitem():
    data = DataBase(1, "192.168.2.11")
    print('data["address"]', data["address"])
    print('data["aaa"]', data["aaa"])
    print('data["id"]', data["id"])

def match_demo():
    point = (2, 0)
    match point:
        case (0, 0):
            print("Origin")
        case (x, 0):
            print(f"On the x-axis at x={x}")
        case (0, y):
            print(f"On the y-axis at y={y}")
        case (x, y):
            print(f"Coordinates: x={x}, y={y}")
        case _:
            print("This should never happen")


if __name__ == "__main__":
    param = input("input: ")

    match param:
        case "enter":
            enter()
        case "getitem":
            getitem()
        case "match_demo":
            match_demo()
        case _:
            pass
