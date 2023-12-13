import threading
import time
import json

class MessageManager:
    def __init__(self, socket, broadcast_ip, port, retransmit_interval=5):
        self.sock = socket
        self.broadcast_ip = broadcast_ip
        self.port = port
        self.retransmit_interval = retransmit_interval
        self.unacknowledged_messages = {}
        self.offline_messages = {}
        self.lock = threading.Lock()

    def send_message(self, message, clock):
        message_id = self._generate_message_id(message, clock)
        message_with_clock = (message, clock, message_id)
        self._send_with_ack(message_with_clock)
        self._start_retransmission_thread(message_with_clock)

    def receive_ack(self, message_id):
        with self.lock:
            if message_id in self.unacknowledged_messages:
                del self.unacknowledged_messages[message_id]

    def store_offline_message(self, addr, message, clock):
        with self.lock:
            self.offline_messages.setdefault(addr, []).append((message, clock))

    def retrieve_offline_messages(self, addr):
        with self.lock:
            return self.offline_messages.pop(addr, [])

    def _send_with_ack(self, message_with_clock):
        self.sock.sendto(json.dumps(message_with_clock).encode(), (self.broadcast_ip, self.port))

    def _start_retransmission_thread(self, message_with_clock):
        thread = threading.Thread(target=self._retransmit_message, args=(message_with_clock,))
        thread.daemon = True
        thread.start()

    def _retransmit_message(self, message_with_clock):
        while True:
            with self.lock:
                if message_with_clock[2] not in self.unacknowledged_messages:
                    break
                self._send_with_ack(message_with_clock)
            time.sleep(self.retransmit_interval)

    def _generate_message_id(self, message, clock):
        return hash((message, json.dumps(clock)))

