# joblib是一个并行计算包，提高代码运行效率
# parallel对象会创建一个进程池，以便在多进程中执行每一个列表项。
# parallel默认情况下使用多进程，n_jobs代表进程数

from joblib import Parallel, delayed

# 对0-9的每个数进行开方运算
Parallel(n_jobs=10)(delayed(sqrt)(i) for i in range(10))

# delayed: 创建元组（functions, args, kwargs）这里的functions就对应上面使用的sqrt，也可以自己定义并传入参数。
# 核心思想是把代码写成生成器表达式


# sklearn中也包括parallel 
from sklearn.utils import parallel_backend

with parallel_backend('multiprocessing'): #也可设置为 threading
  print(Parallel(n_jobs=10)(delayed(sqrt)(i) for i in range(10)))
  
