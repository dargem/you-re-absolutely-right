from collections import defaultdict
import queue, time

seconds_ts = time.time()

# Maintains a queue with a given max size. Elements > 1m get deleted. 
# If the queue is full you cannot add to it. Adding to a full queue is considered "spams"
class SpamBuffer:
    def __init__(self, max_req_m = 5):
        # Maps username -> queue[floats of call time, got by time.time()]
        self.calls: defaultdict[str, queue.Queue[float]] = defaultdict(queue.Queue(max_req_m))

    # Try to add a name to the spam buffer, if adding fails this is considered "spam"
    def add(self, name: str) -> bool:
        current = time.time() # Current time in seconds

        with self.calls[name].mutex:
            while not self.calls[name].empty():
                if self.calls[name][0] + 60 >= current:
                    break # Early ret if < 1m old

                self.calls[name].get() # pop

            if self.calls[name].full(): return False
            self.calls[name].put(current)
            return True