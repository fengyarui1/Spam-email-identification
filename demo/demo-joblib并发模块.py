from joblib import Parallel, delayed
from tqdm import tqdm
import multiprocessing
import time


def test():
    # 获取CPU数量
    cpu_count = multiprocessing.cpu_count()

    # 定义一个简单的耗时任务
    def task(i):
        time.sleep(1)  # 模拟耗时操作
        return i * i

    # 创建任务列表
    tasks = [delayed(task)(i) for i in range(cpu_count * 2)]

    # 使用tqdm显示进度条的并行处理
    results = Parallel(n_jobs=cpu_count)(
        tqdm(tasks, total=len(tasks), desc="Processing tasks")
    )

    print("\n处理结果:", results)


if __name__ == '__main__':
    test()