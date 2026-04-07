from traffic_generator import Packet, TrafficGenerator
from metrics import MetricsManager
from algorithms import PriorityQueue, REDQueue, WFQQueue, WFQScheduler

# ---------------------- Simulation engine ----------------------
def run_simulation(sim_time=100, algorithm="PQ", max_q=20):
    flow_types = ["network_control", "realtime", "critical_data", "best_effort"]
    
    # Custom rates per flow type
    rates = {
        "network_control": 0.1,
        "realtime": 0.4,
        "critical_data": 0.6,
        "best_effort": 1.2
    }
    
    tg = TrafficGenerator(lambdas=rates)
    metrics = MetricsManager(flow_types)

    if algorithm == "PQ":
        queue = PriorityQueue(max_q)
        scheduler = None
    elif algorithm == "RED":
        queue = REDQueue(max_q)
        scheduler = None
    elif algorithm == "WFQ":
        # Weights decide the priority order
        weights = {
            "network_control": 10,
            "realtime": 5,
            "critical_data": 2,
            "best_effort": 1
        }
        queue = WFQQueue(max_q, weights)
        scheduler = WFQScheduler(flow_types)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    for t in range(sim_time):
        # 1. Packet Arrival
        new_packets = tg.generate(t)
        metrics.record_generated(new_packets)
        
        for p in new_packets:
            success = queue.enqueue(p)
            if not success:
                metrics.record_drop(p)
        
        # 2. Packet Processing
        if algorithm == "WFQ":
            packet = scheduler.select_packet(queue)
        else:
            packet = queue.dequeue()
            
        if packet:
            metrics.record_delivery(packet, t)

    return metrics

import argparse

def print_report(algo_name, metrics):
    print(f"\n{'='*10} {algo_name} Results {'='*10}")
    data = []
    for ft, m in metrics.flows.items():
        data.append([ft, f"{m.avg_delay:.2f}", m.throughput, f"{m.loss_rate*100:.2f}%"])
    
    headers = ["Flow Type", "Avg Delay", "Throughput", "Loss Rate"]
    try:
        from tabulate import tabulate
        print(tabulate(data, headers=headers, tablefmt="grid"))
    except ImportError:
        print(f"{'Flow Type':<16} | {'Avg Delay':<10} | {'Throughput':<10} | {'Loss Rate':<10}")
        print("-" * 55)
        for row in data:
            print(f"{row[0]:<16} | {row[1]:<10} | {row[2]:<10} | {row[3]:<10}")

def compare_algorithms(sim_time=200):
    algos = ["PQ", "WFQ", "RED"]
    results = {}
    for algo in algos:
        results[algo] = run_simulation(sim_time=sim_time, algorithm=algo)
        print_report(algo, results[algo])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QoS Packet Scheduling Simulator")
    parser.add_argument("--time", type=int, default=200, help="Simulation time steps")
    parser.add_argument("--max_q", type=int, default=20, help="Maximum queue size")
    
    args = parser.parse_args()
    
    print(f"Starting Simulation (Time: {args.time}, Max Queue: {args.max_q})")
    compare_algorithms(sim_time=args.time)