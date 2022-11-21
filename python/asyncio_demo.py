import asyncio
import time

async def test1() -> None:
    print(1)
    await asyncio.sleep(1)

async def test2() -> str:
    print(2)
    await asyncio.sleep(2)
    return "qwe"

async def test3() -> dict:
    print(3)
    await asyncio.sleep(3)
    return {"aa": 11}

async def run1() -> None:
    loop = asyncio.get_running_loop()
    task1 = loop.create_task(test1())
    task2 = loop.create_task(test2())
    task3 = loop.create_task(test3())
    task_result1 = await task1
    task_result2 = await task2
    task_result3 = await task3
    print(task_result1, task_result2, task_result3)

async def run2() -> None:
    task = [test1(), test2(), test3()]
    print(f"started at {time.strftime('%X')}")
    result = await asyncio.gather(*task)
    print(f"started at {time.strftime('%X')}")
    print(result)

async def run3() -> None:
    task1 = asyncio.create_task(test1())
    task2 = asyncio.create_task(test2())
    task3 = asyncio.create_task(test3())
    print(f"started at {time.strftime('%X')}")
    task_result1 = await task1
    task_result2 = await task2
    task_result3 = await task3
    print(f"started at {time.strftime('%X')}")
    print(task_result1, task_result2, task_result3)

asyncio.run(run1())
# asyncio.run(run2())
# asyncio.run(run3())