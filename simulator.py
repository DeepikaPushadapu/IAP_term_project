import random

# -------------------- PACKET --------------------
class Packet:
    def __init__(self, pid, arrival_time, size, priority, flow_type):
        self.pid = pid
        self.arrival_time = arrival_time
        self.size = size
        self.priority = priority
        self.flow_type = flow_type


# -------------------- TRAFFIC GENERATOR --------------------
class TrafficGenerator:
    def __init__(self):
        self.packet_id = 0

    def generate(self, current_time):
        packets = []
        num_packets = random.randint(0, 2)

        for _ in range(num_packets):
            flow_type = random.choice(["realtime", "best_effort"])

            if flow_type == "realtime":
                priority = 1
                size = random.randint(50, 100)
            else:
                priority = 2
                size = random.randint(100, 200)

            packet = Packet(
                self.packet_id,
                current_time,
                size,
                priority,
                flow_type
            )

            packets.append(packet)
            self.packet_id += 1

        return packets


# -------------------- FIFO QUEUE --------------------
class Queue:
    def __init__(self, max_size):
        self.buffer = []
        self.max_size = max_size
        self.dropped = 0

    def enqueue(self, packet):
        if len(self.buffer) >= self.max_size:
            self.dropped += 1
            return False
        self.buffer.append(packet)
        return True

    def dequeue(self):
        if self.buffer:
            return self.buffer.pop(0)
        return None


# -------------------- FIFO SCHEDULER --------------------
class Scheduler:
    def select_packet(self, queue):
        return queue.dequeue()


# -------------------- METRICS --------------------
class Metrics:
    def __init__(self):
        self.total_delay = 0
        self.delivered = 0
        self.generated = 0

    def record_delivery(self, packet, current_time):
        delay = current_time - packet.arrival_time
        self.total_delay += delay
        self.delivered += 1

    def record_generated(self, count):
        self.generated += count

    def report(self):
        avg_delay = self.total_delay / self.delivered if self.delivered else 0
        throughput = self.delivered
        loss_rate = (self.generated - self.delivered) / self.generated if self.generated else 0

        return avg_delay, throughput, loss_rate


# -------------------- SIMULATION --------------------
def run_simulation(sim_time=50):

    tg = TrafficGenerator()
    queue = Queue(max_size=10)
    scheduler = Scheduler()
    metrics = Metrics()

    for t in range(sim_time):

        # Generate packets
        packets = tg.generate(t)
        metrics.record_generated(len(packets))

        # Enqueue packets
        for p in packets:
            queue.enqueue(p)

        # Dequeue and process one packet
        packet = scheduler.select_packet(queue)

        if packet:
            metrics.record_delivery(packet, t)

    return metrics.report()


# -------------------- MAIN --------------------
if __name__ == "__main__":

    avg_delay, throughput, loss = run_simulation()

    print("---- FIFO SIMULATION ----")
    print("Average Delay:", avg_delay)
    print("Throughput:", throughput)
    print("Packet Loss Rate:", loss)