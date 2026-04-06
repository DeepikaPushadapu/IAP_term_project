import random
import math

class Packet:
    def __init__(self, pid, arrival_time, size, priority, flow_type):
        self.pid = pid
        self.arrival_time = arrival_time
        self.size = size
        self.priority = priority
        self.flow_type = flow_type
        self.wait_time = 0

class TrafficGenerator:
    def __init__(self, lambdas=None):
        self.packet_id = 0
        # lambdas: average packets per time step for each flow type
        self.lambdas = lambdas if lambdas else {
            "network_control": 0.2, 
            "realtime": 0.5, 
            "critical_data": 0.8, 
            "best_effort": 1.5
        }

    def generate(self, current_time):
        packets = []
        for flow_type, rate in self.lambdas.items():
            # 1. Time-Varying Traffic (Example for best_effort)
            actual_rate = rate
            if flow_type == "best_effort":
                # High load for first 25 steps of every 50
                if current_time % 50 < 25:
                    actual_rate = rate * 2.0
                else:
                    actual_rate = rate * 0.5

            # 2. True Poisson Distribution
            L = math.exp(-actual_rate)
            num_packets = 0
            p = 1.0
            while p > L:
                num_packets += 1
                p *= random.random()
            num_packets -= 1

            # 3. Add Bursty Traffic (10% chance for extra packets)
            if random.random() < 0.1:
                num_packets += random.randint(2, 5)
            
            for _ in range(num_packets):
                if flow_type == "network_control":
                    priority = 7  # Highest (6-7)
                    size = random.randint(64, 128)
                elif flow_type == "realtime":
                    priority = 5  # High (4-5)
                    size = random.randint(128, 256)
                elif flow_type == "critical_data":
                    priority = 3  # Medium (2-3)
                    size = random.randint(256, 1024)
                else: # best_effort
                    priority = 1  # Low (0-1)
                    size = random.randint(512, 1500)

                packet = Packet(self.packet_id, current_time, size, priority, flow_type)
                packets.append(packet)
                self.packet_id += 1
        return packets
