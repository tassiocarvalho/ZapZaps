class VectorClock:
    def __init__(self):
        self.timestamps = {}

    def update(self, node_id, timestamp):
        self.timestamps[node_id] = timestamp

    def get_timestamp(self, node_id):
        return self.timestamps.get(node_id, 0)

    def increment(self, node_id):
        self.timestamps[node_id] = self.get_timestamp(node_id) + 1

    def merge(self, other):
        for node, timestamp in other.items():
            self.timestamps[node] = max(self.get_timestamp(node), timestamp)
