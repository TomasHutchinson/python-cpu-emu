import time

debug_cache_hit = False

class RAM:
    def __init__(self, size, delay=0.0):
        self.memory = [0] * size
        self.delay = delay  # seconds

    def read(self, addr):
        if self.delay > 0:
            time.sleep(self.delay)
        return self.memory[addr]

    def write(self, addr, value):
        if self.delay > 0:
            time.sleep(self.delay)
        self.memory[addr] = value
    
    def __len__(self):
        return len(self.memory)
    
    def __str__(self):
        return str(self.memory)


class Cache:
    def __init__(self, size, lower_memory, delay=0.0):
        self.size = size                # max number of entries in cache
        self.lower_memory = lower_memory
        self.data = {}                  # addr -> value
        self.lru_order = []             # list of addresses, most recently used at end
        self.delay = delay              # seconds

    def read(self, addr):
        # Cache hit
        if addr in self.data:
            if debug_cache_hit: print("Cache Hit: {addr}")
            if self.delay > 0:
                time.sleep(self.delay)
            self._mark_used(addr)
            return self.data[addr]

        # Cache miss: fetch from lower memory
        if debug_cache_hit: print("Cache Miss: {addr}")
        value = self.lower_memory.read(addr)
        self._insert(addr, value)
        return value

    def write(self, addr, value):
        # Write-through: store in cache and lower memory
        self._insert(addr, value)
        self.lower_memory.write(addr, value)

    def _insert(self, addr, value):
        # Evict LRU if needed
        if addr not in self.data and len(self.data) >= self.size:
            lru_addr = self.lru_order.pop(0)
            del self.data[lru_addr]

        # Insert or update
        self.data[addr] = value
        self._mark_used(addr)

    def _mark_used(self, addr):
        # Move addr to end = most recently used
        if addr in self.lru_order:
            self.lru_order.remove(addr)
        self.lru_order.append(addr)

    def __len__(self):
        return self.size
    
    def __str__(self):
        string = ""
        arr = list(self.data.keys())
        string = string + str(arr) + "\n"
        string = string + str(self.lower_memory)
        return string
