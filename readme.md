# QoS-Aware Packet Scheduling Simulator

## Overview
This simulator models and evaluates Quality of Service (QoS)-aware packet scheduling algorithms. It demonstrates how different queuing strategies handle multi-priority traffic under realistic, stochastic network conditions.

## Key Features
- **Modular Architecture**: Separate components for traffic generation, scheduling algorithms, and metrics analysis.
- **Algorithms Supported**:
    - **Priority Queuing (PQ)**: Strict priority-based scheduling.
    - **Weighted Fair Queuing (WFQ)**: Guaranteed bandwidth sharing based on weights.
    - **Random Early Detection (RED)**: Congestion avoidance with probabilistic packet drops.
- **Realistic Traffic Models**: Models include Poisson arrivals, bursty spikes, and time-varying loads across 4 priority levels.
- **Comprehensive Metrics**: Tracks average delay, throughput, and packet loss rate per flow.

## Project Structure
- `simulator.py`: Main entry point characterizing the simulation loop.
- `traffic_generator.py`: Generates stochastic network traffic flows.
- `algorithms.py`: Implementation of PQ, WFQ, and RED scheduling logic.
- `metrics.py`: Collection and aggregation of performance data.

## Usage
To run the simulation and compare algorithms:
```bash
python simulator.py --time 500 --max_q 20
```

### Command-line Arguments
- `--time`: Duration of the simulation in time steps (default: 200).
- `--max_q`: Maximum capacity of the packet queue (default: 20).

## Results Comparison
The simulator compares the performance of PQ, WFQ, and RED across four flow types:
1. **Network Control** (Priority 7) - Highest priority.
2. **Real-time** (Priority 5) - VoIP/Video.
3. **Critical Data** (Priority 3) - Business-critical apps.
4. **Best-effort** (Priority 1) - Standard traffic.
