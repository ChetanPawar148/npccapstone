#!/usr/bin/env python3
"""
===============================================================================
NPC CAPSTONE PROJECT: SAFE TEST CLIENT FOR BIND-SHELL SIMULATION
===============================================================================
Student Name    : Chetan Pawar
PRN Number      : 2125UCSM1037
Course          : B.Tech Computer Science Engineering (Cyber Security)
Institution     : Sanjivani University, Kopargaon
Subject         : NPC Capstone Project

SECURITY & ETHICAL NOTICE:
--------------------------
This script is a HARMLESS client utility intended strictly to communicate
with the local educational bind-shell simulation on 127.0.0.1:54321.
It does not connect to external networks, perform exploitation, or transmit
sensitive host data.
===============================================================================
"""

import socket
import sys

HOST = "127.0.0.1"
PORT = 54321
BUFFER_SIZE = 2048

def run_client():
    print("=" * 65)
    print(" NPC CAPSTONE: SAFE TEST CLIENT FOR BIND-SHELL SIMULATION")
    print(" Author: Chetan Pawar (PRN: 2125UCSM1037)")
    print("=" * 65)
    print(f"[*] Attempting connection to local simulation server at {HOST}:{PORT}...")

    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((HOST, PORT))
        print(f"[+] Connected successfully to {HOST}:{PORT}\n")
    except ConnectionRefusedError:
        print(f"[!] Connection failed: Server is not running on {HOST}:{PORT}.")
        print("[!] Please start 'python3 server.py' in a separate terminal first.")
        sys.exit(1)
    except Exception as exc:
        print(f"[!] Network error: {exc}")
        sys.exit(1)

    try:
        # Receive initial banner and prompt
        banner = client_sock.recv(BUFFER_SIZE).decode("utf-8", errors="replace")
        print(banner, end="")

        while True:
            try:
                user_input = input()
            except (EOFError, KeyboardInterrupt):
                print("\n[*] Exiting client session...")
                break

            if not user_input.strip():
                continue

            # Send command to server
            client_sock.sendall((user_input.strip() + "\n").encode("utf-8"))

            # Receive and display response
            response = client_sock.recv(BUFFER_SIZE).decode("utf-8", errors="replace")
            print(response, end="")

            if user_input.strip().upper() == "EXIT":
                print("[*] Server acknowledged exit. Terminating client cleanly.")
                break

    except Exception as run_err:
        print(f"[!] Session error: {run_err}")
    finally:
        client_sock.close()
        print("[+] Client connection closed.")

if __name__ == "__main__":
    run_client()
