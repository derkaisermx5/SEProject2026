# Small testing tool: pretends to be the laser tag equipment.
# Listens on port 7500 and prints everything the game broadcasts
# (equipment IDs, 202 start, 221 end). Type "a:b" and press Enter to send
# a hit event back to the game on port 7501.
#
#   python udp_test_listener.py                 # uses 127.0.0.1
#   python udp_test_listener.py 192.168.1.20    # use a different network

import socket
import sys
import threading

from udp_network import BROADCAST_PORT, RECEIVE_PORT, DEFAULT_NETWORK, validate_network

network = validate_network(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_NETWORK

listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen.bind(("" if network.endswith(".255") else network, BROADCAST_PORT))

send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


def listen_loop():
    while True:
        data, addr = listen.recvfrom(1024)
        print(f"<- received '{data.decode()}' from {addr[0]}:{addr[1]}", flush=True)


threading.Thread(target=listen_loop, daemon=True).start()
print(f"Listening on {network}:{BROADCAST_PORT}. Type a message to send to {network}:{RECEIVE_PORT} (Ctrl+C to quit).")
try:
    for line in sys.stdin:
        line = line.strip()
        if line:
            send.sendto(line.encode(), (network, RECEIVE_PORT))
            print(f"-> sent '{line}'")
except KeyboardInterrupt:
    pass
