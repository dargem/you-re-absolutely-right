from collections import defaultdict, deque
import time
from threading import Lock

# Maintains a queue with a given max size. Elements > 1m get deleted. 
# If the queue is full you cannot add to it. Adding to a full queue is considered "spams"
class SpamBuffer:
    # max_req per dur, managed by a queue
    def __init__(self, max_req = 4, dur = 40):
        # Maps username -> deque[floats of call time, got by time.monotonic()]
        self.calls: defaultdict[str, deque[float]] = defaultdict(lambda: deque(maxlen=max_req))
        self.dur = dur

        # Global lock for all names, can change this to be name level to get a more fine grained version if needed
        self.lock = Lock() 

    # Try to add a name to the spam buffer, if adding fails this is considered "spam"
    def add(self, name: str) -> bool:
        current = time.monotonic() # Current time in seconds

        with self.lock:
            dq = self.calls[name]
            while dq: # Falsy if empty
                if dq[0] + self.dur >= current:
                    break # Early ret if < 1m old

                dq.popleft()

            if len(dq) == dq.maxlen: return False
            dq.append(current)
            return True