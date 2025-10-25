from collections import OrderedDict
import random
import time

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def invalidate(self, idx):
        keys_to_remove = [key for key in self.cache if key[0] <= idx <= key[1]]
        for key in keys_to_remove:
            del self.cache[key]

class RangeQueryProcessor:
    def __init__(self, array, cache_capacity=1000):
        self.array = array
        self.cache = LRUCache(cache_capacity)

    def range_sum(self, L, R):
        key = (L, R)
        cached = self.cache.get(key)
        if cached is not None:
            return cached
        total = sum(self.array[L:R+1])
        self.cache.put(key, total)
        return total

    def update(self, idx, value):
        self.array[idx] = value
        self.cache.invalidate(idx)


# 100_000
N = 100_000
array = [random.randint(1, 1000) for _ in range(N)]
# 50_000
popular_ranges = [(10, 500), (1000, 2000), (50000, 70000)]

queries = []
for _ in range(50000):
    if random.random() < 0.85: # 85 % duplicate
        queries.append(('Range', *random.choice(popular_ranges)))
    else:
        L = random.randint(0, N - 1000)
        R = L + random.randint(0, 1000)
        queries.append(('Range', L, R))

# nocache
no_cache = array.copy() 
start_time = time.time() # profiler
for query in queries:
    if query[0] == "Range":
        _, L, R = query
        _ = sum(no_cache[L:R+1])
    else:
        _, idx, value = query
        no_cache[idx] = value
no_cache_end_time = time.time() - start_time # profiler

# cache
cache = array.copy()
processor = RangeQueryProcessor(cache, cache_capacity=1000)
start_time = time.time() # profiler
for query in queries:
    if query[0] == "Range":
        _, L, R = query
        _ = processor.range_sum(L, R)
    else:
        _, idx, value = query
        processor.update(idx, value)
cache_end_time = time.time() - start_time # profiler
print(f"Без кешу: {no_cache_end_time:.2f} с")
print(f"LRU-кеш: {cache_end_time:.2f} с")