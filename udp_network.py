# UDP networking for the laser tag game.
#
#   * Game software BROADCASTS on port 7500 (equipment IDs, start/end codes)
#   * Game software RECEIVES on port 7501 from any IP (hit / base-score events)
#   * Default network address is 127.0.0.1, and it can be changed at runtime
#     with set_network() (F2 on the player entry screen, or --network on the
#     command line).

import ipaddress
import queue
import socket
import threading

DEFAULT_NETWORK = "127.0.0.1"
BROADCAST_PORT = 7500      # we send to this port
RECEIVE_PORT = 7501        # we listen on this port
BUFFER_SIZE = 1024

# Special codes used by the game
CODE_START_GAME = 202
CODE_END_GAME = 221
CODE_RED_BASE_SCORED = 53
CODE_GREEN_BASE_SCORED = 43


def validate_network(address):
    """Return the address as a clean string, or raise ValueError if it isn't a valid IPv4 address."""
    address = str(address).strip()
    ip = ipaddress.ip_address(address)          # raises ValueError if invalid
    if ip.version != 4:
        raise ValueError(f"{address} is not an IPv4 address")
    return str(ip)


def local_network_choices():
    """Addresses worth offering in the 'select network' dropdown."""
    choices = [DEFAULT_NETWORK]
    # IP of the interface the OS would use to reach the outside world.
    # (UDP connect() doesn't actually send any packets.)
    try:
        probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        probe.connect(("10.255.255.255", 1))
        choices.append(probe.getsockname()[0])
        probe.close()
    except OSError:
        pass
    try:
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
            choices.append(ip)
    except OSError:
        pass
    choices.append("255.255.255.255")
    # remove duplicates while keeping order
    seen = []
    for c in choices:
        if c not in seen:
            seen.append(c)
    return seen


class UDPNetwork:
    def __init__(self, network=DEFAULT_NETWORK, on_receive=None):
        """
        network    -- IPv4 address to broadcast to / listen on
        on_receive -- optional callback(message_str, sender_addr); it runs on the
                      receiver thread, so GUI code should use get_messages()
                      (polled with tk.after) instead of touching widgets here.
        """
        self.network = validate_network(network)
        self.on_receive = on_receive
        self.messages = queue.Queue()
        self._lock = threading.Lock()
        self._send_sock = None
        self._recv_sock = None
        self._recv_thread = None
        self._running = False
        self._open_sockets()

    # ---------- socket setup ----------
    def _open_sockets(self):
        # Transmit socket (broadcast enabled so 255.255.255.255 / x.x.x.255 work too)
        self._send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Receive socket on port 7501, bound to 0.0.0.0 so data from ANY ip
        # address is accepted (per the project requirements).
        self._recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._recv_sock.settimeout(0.5)   # lets the thread notice when we close
        bind_ip = ""
        self._recv_sock.bind((bind_ip, RECEIVE_PORT))

        self._running = True
        self._recv_thread = threading.Thread(target=self._receive_loop, daemon=True)
        self._recv_thread.start()
        print(f"[UDP] Broadcasting to {self.network}:{BROADCAST_PORT}, "
              f"receiving on {bind_ip or '0.0.0.0'}:{RECEIVE_PORT}")

    def _close_sockets(self):
        self._running = False
        if self._recv_thread is not None:
            self._recv_thread.join(timeout=2)
        for s in (self._send_sock, self._recv_sock):
            if s is not None:
                s.close()
        self._send_sock = self._recv_sock = self._recv_thread = None

    def _receive_loop(self):
        sock = self._recv_sock
        while self._running:
            try:
                data, addr = sock.recvfrom(BUFFER_SIZE)
            except socket.timeout:
                continue
            except OSError:
                break
            message = data.decode(errors="replace").strip()
            print(f"[UDP] Received '{message}' from {addr[0]}:{addr[1]}")
            self.messages.put((message, addr))
            if self.on_receive:
                self.on_receive(message, addr)

    # ---------- public API ----------
    def set_network(self, address):
        """Switch to a different network address. Raises ValueError / OSError on failure
        (in which case the previous network is kept)."""
        new_address = validate_network(address)
        with self._lock:
            old_address = self.network
            self._close_sockets()
            self.network = new_address
            try:
                self._open_sockets()
            except OSError:
                # couldn't bind on the new address -> go back to the old one
                self.network = old_address
                self._open_sockets()
                raise
        return self.network

    def broadcast(self, message):
        """Send a message (int or str) to <network>:7500."""
        payload = str(message).encode()
        with self._lock:
            self._send_sock.sendto(payload, (self.network, BROADCAST_PORT))
        print(f"[UDP] Broadcast '{message}' to {self.network}:{BROADCAST_PORT}")

    def broadcast_equipment_id(self, equipment_id):
        """Called after each player is added."""
        equipment_id = int(equipment_id)
        self.broadcast(equipment_id)

    def broadcast_start(self):
        self.broadcast(CODE_START_GAME)

    def broadcast_end(self):
        for _ in range(3):              # end code is sent three times
            self.broadcast(CODE_END_GAME)

    def get_messages(self):
        """Return (and clear) all messages received since the last call."""
        items = []
        while True:
            try:
                items.append(self.messages.get_nowait())
            except queue.Empty:
                return items

    def close(self):
        with self._lock:
            self._close_sockets()
        print("[UDP] Sockets closed")
