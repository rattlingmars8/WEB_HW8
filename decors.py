import time
from functools import wraps
import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host="localhost", port=6379, password=None) # Порт 6379, бо контейнер запускався як у конспекті
cache = RedisLRU(client)


def cache_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # ключ для кешування на основі назви функції та переданих аргументів
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            # Перевіряємо, чи є результат у кеші
            cached_result = cache.get(cache_key)

            if cached_result is not None:
                print("Result retrieved from cache.")
                return cached_result
            #  Викликаємо функцію, та зберігаємо результат у кеш, на майбутнє
            result = func(*args, **kwargs)
            if result:
                cache.set(cache_key, result)

            return result

        except redis.exceptions.ConnectionError:
            print("Warning! Redis connection error.")

    return wrapper


def time_of(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function {func.__name__} executed in {execution_time:.4f} seconds")
        return result
    return wrapper


def handle_empty_result(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if not result:
            return []
        return result

    return wrapper
