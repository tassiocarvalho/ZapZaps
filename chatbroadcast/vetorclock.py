class VectorClock:
    def __init__(self, id):
        self.id = id
        self.clock = {}

    def tick(self):
        self.clock[self.id] = self.clock.get(self.id, 0) + 1

    def update(self, incoming_clock):
        for node, timestamp in incoming_clock.items():
            self.clock[node] = max(self.clock.get(node, 0), timestamp)
        self.tick()

    def as_dict(self):
        return self.clock

    def is_concurrent(self, other_clock):
        for node in set(self.clock.keys()).union(other_clock.keys()):
            if self.clock.get(node, 0) != other_clock.get(node, 0):
                return False
        return True

    def is_causally_after(self, other_clock):
        after = False
        for node, timestamp in other_clock.items():
            if self.clock.get(node, 0) < timestamp:
                return False
            if self.clock.get(node, 0) > timestamp:
                after = True
        return after
    
    def is_causally_before(self, other_clock):
        for node, timestamp in other_clock.items():
            if self.clock.get(node, 0) > timestamp:
                return False
        return True

    def copy(self):
        """ Retorna uma cópia do relógio vetorial atual. """
        new_clock = VectorClock(self.id)
        new_clock.clock = self.clock.copy()
        return new_clock

    def is_after(self, other_clock):
        """ Verifica se este relógio vetorial é 'depois' de outro. """
        for node, timestamp in self.clock.items():
            if other_clock.clock.get(node, 0) > timestamp:
                return False
        return True

    def is_causally_after(self, other_clock):
        """ Verifica se este relógio vetorial é causalmente posterior a outro. """
        after = False
        for node, timestamp in other_clock.clock.items():
            if self.clock.get(node, 0) < timestamp:
                return False
            if self.clock.get(node, 0) > timestamp:
                after = True
        return after

    @staticmethod
    def from_dict(clock_dict, id):
        """ Cria um VectorClock a partir de um dicionário e um id. """
        vc = VectorClock(id)
        vc.clock = clock_dict
        return vc
