import random

#---------- Queue base class implementation ----------
class BaseQueue:
    def __init__(self, max_size):
        self.max_size = max_size
        self.buffer = []
        self.dropped_count = 0

    def enqueue(self, packet):
        raise NotImplementedError

    def dequeue(self):
        if self.buffer:
            return self.buffer.pop(0)
        return None

    def is_full(self):
        return len(self.buffer) >= self.max_size


#---------- Priority Queue implementation ----------
class PriorityQueue(BaseQueue):
    def enqueue(self, packet):
        if self.is_full():
            self.dropped_count += 1
            return False
        self.buffer.append(packet)
        # Sort by priority - higher numerical value = higher priority (e.g. 7 > 1)
        self.buffer.sort(key=lambda x: x.priority, reverse=True)
        return True


#---------- RED Queue implementation ----------
class REDQueue(BaseQueue):
    def __init__(self, max_size, min_th=None, max_th=None, max_p=0.1):
        super().__init__(max_size)
        self.min_th = min_th if min_th is not None else int(0.3 * max_size)
        self.max_th = max_th if max_th is not None else int(0.7 * max_size)
        self.max_p = max_p

    def enqueue(self, packet):
        q_len = len(self.buffer)
        
        if q_len >= self.max_size:
            self.dropped_count += 1
            return False
            
        if q_len < self.min_th:
            pass
        elif q_len >= self.max_th:
            self.dropped_count += 1
            return False
        else:
            prob = self.max_p * (q_len - self.min_th) / (self.max_th - self.min_th)
            if random.random() < prob:
                self.dropped_count += 1
                return False
        
        self.buffer.append(packet)
        return True


#---------- WFQ Queue implementation ----------
class WFQQueue:
    def __init__(self, max_size, weights):
        self.max_size = max_size
        self.weights = weights
        self.queues = {ft: [] for ft in weights.keys()}
        self.dropped_count = 0

    def enqueue(self, packet):
        total_len = sum(len(q) for q in self.queues.values())
        if total_len >= self.max_size:
            self.dropped_count += 1
            return False
        self.queues[packet.flow_type].append(packet)
        return True
    

#---------- WFQ Scheduler implementation ----------
class WFQScheduler:
    def __init__(self, flow_types):
        self.flow_types = flow_types
        self.current_flow_idx = 0
        self.counter = 0

    def select_packet(self, wfq_queue):
        for _ in range(len(self.flow_types)):
            ft = self.flow_types[self.current_flow_idx]
            if wfq_queue.queues[ft] and self.counter < wfq_queue.weights[ft]:
                self.counter += 1
                return wfq_queue.queues[ft].pop(0)
            else:
                self.counter = 0
                self.current_flow_idx = (self.current_flow_idx + 1) % len(self.flow_types)
        return None
