# Safe Educational Bind-Shell Simulation

**Author:** Chetan Pawar  
**PRN:** 2125UCSM1037  
**Department:** Computer Science Engineering (Cyber Security), Sanjivani University  
**Subject:** NPC Capstone Project — Malware Analysis Sandbox  

---

## 1. Purpose and Overview

This module provides a strictly harmless, educational simulation of client-server socket communication mimicking the architectural model of a bind shell. It allows cybersecurity students to study process table dynamics, network socket binding, port listening states, and forensic cleanup without exposing the sandbox or host to the severe risks of genuine malicious backdoors or unrestricted command-execution payloads.

---

## 2. Security Design Principles & Safeguards

### What the Program Does
* **Binds Exclusively to Loopback:** Listens exclusively on `127.0.0.1` (TCP port `54321`). No network traffic can be received from or sent to physical LAN adapters, external virtual bridges, or the host machine.
* **Predefined Benign Commands Only:** Recognizes strictly three fixed, non-destructive commands:
  * `STATUS`: Displays current server timestamp, uptime, interface binding, and sandbox isolation status.
  * `HELP`: Displays command usage instructions.
  * `EXIT`: Gracefully disconnects the active client session and returns the server to its listening state.
* **Inspectable Process & Port:** Creates observable entries in `ps aux`, `top`, `ss -tulpn`, and `/proc/<pid>/` for students to practice operating system triage and process monitoring.
* **Clean Session Lifecycle:** Can be terminated cleanly via standard signals (`SIGINT` / `Ctrl+C`), releasing network socket resources immediately.

### What the Program Does NOT Do
* **NO Arbitrary Command Execution:** Absolutely NO calls to `os.system()`, `subprocess.Popen()`, `os.popen()`, `eval()`, `exec()`, or standard shells (`/bin/sh`, `/bin/bash`). Commands like `ls`, `cat /etc/passwd`, `rm -rf`, or arbitrary system binaries are rejected with a safety warning.
* **NO Persistence or Autostart:** Does NOT register cron jobs, systemd services, registry keys, init scripts, or shell configuration hooks (`.bashrc`).
* **NO Privilege Escalation:** Runs strictly under normal unprivileged user privileges without requesting `sudo` or modifying system permissions.
* **NO File System Destruction or Credential Stealing:** Does not scan disk drives, access browser profiles, read sensitive directories, or write hidden dropper files.
* **NO Remote Weaponization:** Cannot be accessed outside the virtual machine because external binding (`0.0.0.0`) is prohibited in the code.

---

## 3. Communication Architecture

```
+-------------------------------------------------------------------+
|               Linux Sandbox Virtual Machine (Isolated)             |
|                                                                   |
|   +-----------------------+              +--------------------+   |
|   |                       |  TCP Socket  |                    |   |
|   |  safe_test_client.py  |<============>|  safe_server.py    |   |
|   |  (Local Client)       |  127.0.0.1:  |  (Loopback Server) |   |
|   |                       |    54321     |  Listening on lo   |   |
|   +-----------------------+              +--------------------+   |
|                                                                   |
|   Network Interface: lo (127.0.0.1/8)                             |
|   Physical Adapters: Disconnected / Host-Only / Internal Only     |
+-------------------------------------------------------------------+
```

* **Interface:** `lo` (Linux Loopback Adapter, `127.0.0.1`)
* **Transport Protocol:** Transmission Control Protocol (TCP)
* **Port:** `54321` (Non-privileged, unassigned port above 1024)
* **Transmission Nature:** Loopback packets travel exclusively across the kernel networking stack and do not cross any virtual or physical wire.

---

## 4. Execution and Verification Guide

### Step 1: Starting the Safe Server
In your first terminal inside the Linux VM:
```bash
python3 server.py
```
*Expected Output:*
```
=================================================================
 NPC CAPSTONE: SAFE BIND-SHELL SIMULATION SERVER
 Author: Chetan Pawar (PRN: 2125UCSM1037)
=================================================================
[*] Initializing local TCP socket...
[*] Binding strictly to loopback interface: 127.0.0.1:54321
[+] Server successfully listening on TCP 127.0.0.1:54321
[*] Monitoring target ready: Use 'ss -tulpn' or 'ps aux' to observe.
[*] Press Ctrl+C in this terminal to terminate server gracefully.
```

### Step 2: Observing the Listening Port (Triage Terminal)
In a second terminal, verify that the server is listening strictly on `127.0.0.1` and NOT `0.0.0.0`:
```bash
ss -tulpn | grep 54321
```
*Expected Output:*
```
tcp   LISTEN 0      1      127.0.0.1:54321      0.0.0.0:*    users:(("python3",pid=XXXX,fd=3))
```

### Step 3: Starting the Safe Client
In a third terminal (or after checking triage), connect locally:
```bash
python3 client.py
```
*Available Commands to Test:*
```
SAFE-SHELL> STATUS
SAFE-SHELL> HELP
SAFE-SHELL> whoami        <-- Observe rejection message demonstrating safety
SAFE-SHELL> EXIT
```

### Step 4: Stopping the Simulation
Press `Ctrl+C` in the server terminal. Re-run `ss -tulpn | grep 54321` to verify the socket has closed.

---

## 5. Distinction: Simulation vs. Actual Malware

| Attribute | Educational Safe Simulation (`server.py`) | Real Malicious Bind/Reverse Shell |
| :--- | :--- | :--- |
| **Bound Interface** | Strictly `127.0.0.1` (Loopback only) | `0.0.0.0` or connects out to attacker C2 |
| **Command Execution**| Hardcoded benign responses (`STATUS`, `HELP`) | Unrestricted shell execution (`/bin/sh -i`) |
| **System Modification**| None; zero persistence or file writes | Often installs cron jobs, drops rootkits |
| **Network Traffic** | Local kernel loopback only | External TCP/UDP/DNS tunneling to C2 |
| **VirusTotal Status** | Benign script; 0 detections or unindexed | Flagged by multiple AV/EDR signatures |

> **Academic Note:** If an academic instructor requires analyzing a functional reverse shell or live sample, students must obtain an instructor-approved benign training binary (e.g., within an authorized Metasploitable lab), conduct the experiment under strict supervisor guidance, and never deploy weaponized payloads.
