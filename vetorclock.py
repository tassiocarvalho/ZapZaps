class VetorClock:
    def __init__(self):
        self.clock = {}

    def update(self, member, timestamp):
        self.clock[member] = max(self.clock.get(member, 0), timestamp)

    def increment(self, member):
        self.clock[member] = self.clock.get(member, 0) + 1

    def get_clock(self):
        # Certifique-se de que as chaves sejam strings
        return {f"{ip_port[0]}:{ip_port[1]}": time for ip_port, time in self.clock.items()}

    def compare(self, other):
        # Retorna True se self.clock é menor ou igual a other
        for member, timestamp in self.clock.items():
            if timestamp > other.get(member, 0):
                return False
        return True
