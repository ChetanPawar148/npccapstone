#!/usr/bin/env python3
"""
===============================================================================
NPC CAPSTONE PROJECT: SAFE EDUCATIONAL BIND-SHELL SIMULATION (SERVER)
===============================================================================
Student Name    : Chetan Pawar
PRN Number      : 2125UCSM1037
Course          : B.Tech Computer Science Engineering (Cyber Security)
Institution     : Sanjivani University, Kopargaon
Subject         : NPC Capstone Project

SECURITY & ETHICAL NOTICE:
--------------------------
This script is a HARMLESS, strictly educational laboratory simulation.
It is designed solely to illustrate client-server network socket behavior,
listening port states, process table entries, and connection teardown inside
an isolated virtual machine sandbox.

SAFETY CONSTRAINTS:
1. Binds EXCLUSIVELY to the loopback interface (127.0.0.1). It CANNOT accept
   connections from any external network or host adapter.
2. DOES NOT execute arbitrary operating system commands (NO os.system, NO
   subprocess, NO shell evaluation).
3. Responds ONLY to three hardcoded, predefined benign commands:
   - STATUS : Returns current simulated laboratory status and server uptime.
   - HELP   : Returns a list of supported safe commands.
   - EXIT   : Closes the active client session gracefully.
4. Contains NO persistence mechanisms, NO autorun features, NO file modifications,
   and NO network transmission beyond the local loopback interface.
===============================================================================
"""

import socket
import sys
import time
from datetime import datetime

# Network Configuration: Local loopback only, non-privileged port
HOST = "127.0.0.1"
PORT = 54321
BUFFER_SIZE = 1024
SERVER_START_TIME = time.time()

BANNER = """
======================================================
  NPC CAPSTONE LAB: SAFE BIND-SHELL SIMULATION v1.0
  Author: Chetan Pawar (PRN: 2125UCSM1037)
  Status: Educational Simulation Active (Loopback Only)
  Type 'HELP' for supported safe commands.
======================================================
"""

def handle_command(cmd_str: str) -> tuple[str, bool]:
    """
    Safely process predefined, non-executable commands.
    Returns: (response_string, should_terminate_session)
    """
    clean_cmd = cmd_str.strip().upper()
    
    if clean_cmd == "HELP":
        help_text = (
            "\n[SAFE SIMULATION COMMAND MENU]\n"
            "  STATUS : Display sandbox environment status and server uptime\n"
            "  HELP   : Display this command reference guide\n"
            "  EXIT   : Disconnect and end client session\n"
            "Note: Arbitrary command execution is disabled by design for safety.\n\n"
        )
        return help_text, False

    elif clean_cmd == "STATUS":
        uptime_seconds = int(time.time() - SERVER_START_TIME)
        status_text = (
            f"\n[SANDBOX ENVIRONMENT STATUS]\n"
            f"  Server Time        : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"  Uptime             : {uptime_seconds} seconds\n"
            f"  Bound Interface    : {HOST} (Strictly Loopback)\n"
            f"  Listening Port     : {PORT} (TCP)\n"
            f"  Isolation Mode     : Isolated Sandbox Simulation\n"
            f"  External Access    : DISABLED / PROHIBITED\n"
            f"  Execution Engine   : Benign Educational Mock\n\n"
        )
        return status_text, False

    elif clean_cmd == "EXIT":
        return "\n[INFO] Closing session. Goodbye.\n", True

    elif clean_cmd == "":
        return "", False

    else:
        warning_msg = (
            f"\n[REJECTED] Unknown or prohibited command: '{clean_cmd}'\n"
            f"Safety Policy: Only 'STATUS', 'HELP', and 'EXIT' are recognized.\n"
            f"Arbitrary system commands are not permitted.\n\n"
        )
        return warning_msg, False

def run_server():
    """Initializes socket, listens on loopback, and processes test sessions."""
    print("=" * 65)
    print(" NPC CAPSTONE: SAFE BIND-SHELL SIMULATION SERVER")
    print(" Author: Chetan Pawar (PRN: 2125UCSM1037)")
    print("=" * 65)
    print(f"[*] Initializing local TCP socket...")
    print(f"[*] Binding strictly to loopback interface: {HOST}:{PORT}")
    
    try:
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen(1)
    except Exception as exc:
        print(f"[!] Socket binding error: {exc}")
        sys.exit(1)

    print(f"[+] Server successfully listening on TCP {HOST}:{PORT}")
    print("[*] Monitoring target ready: Use 'ss -tulpn' or 'ps aux' to observe.")
    print("[*] Press Ctrl+C in this terminal to terminate server gracefully.\n")

    try:
        while True:
            print("[*] Waiting for local test client connection...")
            client_sock, client_addr = server_sock.accept()
            print(f"[+] Connection accepted from {client_addr[0]}:{client_addr[1]}")
            
            # Send initial educational banner
            client_sock.sendall(BANNER.encode("utf-8"))
            client_sock.sendall(b"SAFE-SHELL> ")

            session_active = True
            while session_active:
                try:
                    data = client_sock.recv(BUFFER_SIZE)
                    if not data:
                        print(f"[-] Client {client_addr[0]}:{client_addr[1]} disconnected unexpectedly.")
                        break

                    decoded_input = data.decode("utf-8", errors="replace")
                    response, should_exit = handle_command(decoded_input)
                    
                    if response:
                        client_sock.sendall(response.encode("utf-8"))
                    
                    if should_exit:
                        print(f"[*] Client requested session termination (EXIT).")
                        session_active = False
                    else:
                        client_sock.sendall(b"SAFE-SHELL> ")

                except ConnectionResetError:
                    print(f"[-] Client {client_addr[0]}:{client_addr[1]} reset the connection.")
                    break
                except Exception as inner_err:
                    print(f"[!] Error processing client session: {inner_err}")
                    break

            client_sock.close()
            print(f"[*] Client connection closed. Returning to listening state.\n")

    except KeyboardInterrupt:
        print("\n\n[!] KeyboardInterrupt received. Shutting down safe server gracefully...")
    finally:
        server_sock.close()
        print("[+] Socket closed. Safe simulation completed cleanly.")

if __name__ == "__main__":
    run_server()
