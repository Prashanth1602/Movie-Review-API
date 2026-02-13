import time
from threading import Lock
from typing import Dict, Tuple

class TokenBucket:
    def __init__(self, rate: float, capacity: float):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = Lock()

    def consume(self, tokens: float = 1.0) -> bool:
        with self.lock:
            now = time.time()
            elapsed = now - self.last_refill
            refill_amount = elapsed * self.rate
            self.tokens = min(self.capacity, self.tokens + refill_amount)
            self.last_refill = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

class RateLimiter:
    def __init__(self, rate: float = 1.0, capacity: float = 5.0):
        self.rate = rate
        self.capacity = capacity
        self.buckets: Dict[str, TokenBucket] = {}
        self.lock = Lock()

    def check_rate_limit(self, key: str) -> bool:
        if key not in self.buckets:
            with self.lock:
                if key not in self.buckets:
                    self.buckets[key] = TokenBucket(self.rate, self.capacity)
        
        return self.buckets[key].consume()
