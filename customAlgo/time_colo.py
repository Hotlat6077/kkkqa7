import time
from loguru import logger
import sys
import warnings
from functools import wraps



warnings.filterwarnings("ignore")
logger.remove()
logger.add(sys.stdout, colorize=True, format="<g>{time:HH:MM:ss:SSS}</g> | <c>{level}</c> | <level>{message}</level>")

class TimerDecorator:
    def __init__(self, func):
        self.func = func
        wraps(self.func)(self)
    
    def __call__(self, *args, **kwargs):
        start_time = time.perf_counter()
        result = self.func(*args, **kwargs)
        end_time = time.perf_counter()
        
        execution_time = end_time - start_time
        logger.info(f"[{self.func.__name__}] 执行时间: {execution_time:.6f} 秒")
        #print(f"[{self.func.__name__}] 执行时间: {execution_time:.6f} 秒")
        
        return result
    
    def __get__(self, instance, owner):
        """支持实例方法"""
        return lambda *args, **kwargs: self(instance, *args, **kwargs)

