from collections import defaultdict, deque
import time
from threading import Lock

# Maintains a queue with a given max size. Elements > 1m get deleted. 
# If the queue is full you cannot add to it. Adding to a full queue is considered "spams"
class SpamBuffer:
    def __init__(self, max_req_m = 5):
        # Maps username -> deque[floats of call time, got by time.time()]
        self.calls: defaultdict[str, deque[float]] = defaultdict(lambda: deque(maxlen=max_req_m))
        self.locks: defaultdict[str, Lock] = defaultdict(Lock)

    # Try to add a name to the spam buffer, if adding fails this is considered "spam"
    def add(self, name: str) -> bool:
        current = time.time() # Current time in seconds

        with self.locks[name]:
            dq = self.calls[name]
            while dq: # Falsy if empty
                if dq[0] + 60 >= current:
                    break # Early ret if < 1m old

                dq.popleft()

            if len(dq) == dq.maxlen: return False
            dq.append(current)
            return True