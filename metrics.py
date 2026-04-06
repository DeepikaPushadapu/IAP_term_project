class FlowMetrics:
    def __init__(self):
        self.generated = 0
        self.delivered = 0
        self.dropped = 0
        self.total_delay = 0

    @property
    def avg_delay(self):
        return self.total_delay / self.delivered if self.delivered > 0 else 0

    @property
    def throughput(self):
        return self.delivered

    @property
    def loss_rate(self):
        return self.dropped / self.generated if self.generated > 0 else 0

class MetricsManager:
    def __init__(self, flow_types):
        self.flows = {ft: FlowMetrics() for ft in flow_types}
        self.total_generated = 0

    def record_generated(self, packets):
        for p in packets:
            self.flows[p.flow_type].generated += 1
            self.total_generated += 1

    def record_delivery(self, packet, current_time):
        delay = current_time - packet.arrival_time
        metrics = self.flows[packet.flow_type]
        metrics.delivered += 1
        metrics.total_delay += delay

    def record_drop(self, packet):
        self.flows[packet.flow_type].dropped += 1
