from numba import jit
import random

def func(num):
    acc = 0
    for i in range(num):
        x = random.random()
        y = random.random()
        if (x ** 2 + y ** 2) < 1.0:
            acc += 1
    return 4.0 * acc / num
  
func(10000) #普通运行：8.98 ms

func_jit = jit()(func)
func_jit(10000) #jit加速：0 ns

#-------------------------------------------------
from numba import jit, njit, vectorize  

#原始计算函数
def original_func(input_list):
    output_list = []
    for item in input_list:
        if item % 2 == 0:
            output_list.append(2)
        else:
            output_list.append(1)
    return output_list

test_array = list(range(100000))

# ！！建议总是把nopython=True， 因为numba对于python一些情况下的运行会敏感。numba在不适用的时候，如果不设置nopython=true,只会给出警告而不会报错
# 我们希望numba真正起到加速的作用，最好这么设置，以提醒我们写的是否为有效的加速代码。 ！！另外njit()等价于jit(nopython=True)
jitted_func = jit(nopython=True)(original_func)
res = jitted_func(test_array)


# 然而以上的运行还是会给出警告，并且运行时间会更长。这是因为numba和python的List不是很兼容。
# 我们应该尽量避免使用python的list，而是使用 numpy 的 array。此外，numba 官网给出了一个 from numba.typed import List 供我们进行列表转换
test_array = np.arange(100000)
jitted_func = njit()(original_func)
res = jitted_func(test_array)


# ----------------vectorize的作用：可以把函数重写为 标量计算-----------------------
import numpy as np

@vectorize
def original_func(num):
    if num % 2 == 0:
        return 2
    else:
        return 1
    
test_array = np.arange(100000)    
# 对于上面的函数，我们既可以传入单个数，也可以传入列表，！！并可以同时完成加速任务。
original_func(test_array)
