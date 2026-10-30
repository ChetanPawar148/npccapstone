# Linux System and Process Monitoring Guide

**Student Name:** Chetan Pawar  
**PRN:** 2125UCSM1037  
**Course:** B.Tech Computer Science Engineering (Cyber Security)  
**Institution:** Sanjivani University, Kopargaon  
**Subject:** NPC Capstone Project  
**Academic Year:** 2026–2027  

---

## 1. Objectives of System Monitoring in Malware Sandboxes

Dynamic analysis requires recording the delta (difference) between the uninfected operating system state and the infected or running state. System monitoring provides empirical evidence of:
- **Process Spawning:** What binaries or subprocesses are executed, their command-line arguments, parent process IDs (PPID), and execution hierarchy.
- **Network Sockets:** What network interfaces are targeted, listening ports opened, and active socket connections established.
- **Filesystem Activity:** Creation, modification, or deletion of configuration files, binaries, and temporary scripts.
- **Resource Utilization:** Spikes in CPU or RAM that may indicate cryptomining, infinite loops, or memory consumption.

---

## 2. Core Linux Utilities for Sandbox Triage

The following built-in Linux command-line utilities are used to collect forensic observations during the laboratory experiment:

```
+---------------------------------------------------------------------------------------------------+
|                                LINUX MONITORING UTILITIES TOOLKIT                                 |
+------------+------------------------------------+-------------------------------------------------+
| Utility    | Primary Purpose                    | Key Flags & Recommended Syntax                  |
+------------+------------------------------------+-------------------------------------------------+
| ps         | Process status snapshot            | ps aux, ps -ef --forest, ps -p <PID> -o ...    |
| top        | Real-time process monitoring       | top -b -n 1 (batch mode for log export)         |
| ss         | Modern socket statistics           | ss -tulpn, ss -ti state established             |
| ip         | Interfaces and routing table       | ip addr show, ip route show, ip link show       |
| lsof       | List open files and descriptors    | lsof -p <PID>, lsof -i :54321                   |
| stat       | File timestamps and inode details  | stat server.py, stat /tmp/                      |
| sha256sum  | Cryptographic file hashing         | sha256sum server.py client.py                   |
| /proc      | Kernel pseudo-filesystem           | cat /proc/<PID>/cmdline, ls -l /proc/<PID>/fd   |
+------------+------------------------------------+-------------------------------------------------+
```

---

## 3. Detailed Command Reference and Output Interpretation

### 3.1. Process Inspection: `ps`
`ps` reads process data directly from the kernel `/proc` filesystem.

```bash
# 1. Full process list with user, PID, CPU, memory, and command
ps aux | grep -E "python3|server.py|client.py"

# 2. Hierarchical forest view showing parent-child process relationships
ps -ef --forest
```

*Key Fields to Record:*
- `USER`: The security context (username) under which the process executes.
- `PID`: The unique Process Identifier assigned by the kernel.
- `PPID`: Parent Process ID, exposing which shell or service spawned the process.
- `COMMAND`: The exact command-line invocation including flags and script paths.

### 3.2. Socket Inspection: `ss`
`ss` (Socket Statistics) is the modern, fast replacement for the legacy `netstat` utility.

```bash
# Display all listening TCP (-t) and UDP (-u) sockets with numeric ports (-n) and process info (-p)
ss -tulpn

# Filter specifically for the simulation port
ss -tulpn | grep 54321
```

*Output Interpretation:*
```
Netid  State   Recv-Q  Send-Q  Local Address:Port   Peer Address:Port  Process
tcp    LISTEN  0       1       127.0.0.1:54321      0.0.0.0:*          users:(("python3",pid=14205,fd=3))
```
- `Local Address:Port`: Confirms strictly `127.0.0.1:54321` (safe loopback binding).
- `Process`: Shows process name (`python3`), PID, and file descriptor number (`fd=3`).

### 3.3. Open Files and Descriptors: `lsof` and `/proc/<PID>/fd/`
In Unix systems, everything is treated as a file, including network sockets.

```bash
# List all file descriptors held open by the simulation server
lsof -p <PID>

# Inspect file descriptors directly via kernel procfs
ls -la /proc/<PID>/fd/
```

*What This Reveals:*
- Standard I/O handles (`fd 0`, `fd 1`, `fd 2` pointing to `/dev/pts/X`).
- Network socket handle (`fd 3` pointing to `socket:[XXXXX]`).
- Any configuration, log, or dropper files opened for reading or writing.

### 3.4. File Timestamps & Inode Inspection: `stat`
Forensic analysis tracks file creation and modification timestamps:

```bash
stat lab/safe_shell_simulation/server.py
```

*Output Interpretation:*
- `Size`: Exact byte length of the file on disk.
- `Access (atime)`: When the script was last read or executed.
- `Modify (mtime)`: When the script contents were last written to.
- `Change (ctime)`: When file metadata or permissions were modified.

---

## 4. Empirical Observation Log Templates

Use the following structured tables to record your observations before, during, and after running the experiment in your virtual machine.

### Baseline Observation Table (Before Experiment)

| Observation Time | Tool / Command Used | Actual Observed Result | Interpretation | Screenshot Ref |
| :--- | :--- | :--- | :--- | :--- |
| `[HH:MM:SS]` | `ip addr show` | `lo` is UP; Ethernet adapter disconnected | Sandbox network isolation confirmed | `[Fig 02]` |
| `[HH:MM:SS]` | `ip route show` | No default gateway present | No egress path to WAN | `[Fig 03]` |
| `[HH:MM:SS]` | `ping -c 3 8.8.8.8`| Network unreachable | Internet isolation verified | `[Fig 04]` |
| `[HH:MM:SS]` | `ss -tulpn` | No processes on port 54321 | Clean network baseline | `[Fig 05]` |
| `[HH:MM:SS]` | `ps aux` | Standard system daemons only | Clean process baseline | `[Fig 06]` |

### Post-Experiment Observation Table (During / After Execution)

| Observation Time | Tool / Command Used | Actual Observed Result | Interpretation | Screenshot Ref |
| :--- | :--- | :--- | :--- | :--- |
| `[HH:MM:SS]` | `python3 server.py` | Server bound to `127.0.0.1:54321` | Safe simulation running | `[Fig 07]` |
| `[HH:MM:SS]` | `ss -tulpn` | TCP `127.0.0.1:54321` LISTEN | Listening socket confirmed | `[Fig 08]` |
| `[HH:MM:SS]` | `python3 client.py` | Interactive prompt `SAFE-SHELL>` | Client connected to loopback | `[Fig 09]` |
| `[HH:MM:SS]` | `ps aux` | `python3 server.py` visible | Active PID logged | `[Fig 10]` |
| `[HH:MM:SS]` | `tcpdump -i lo` | 3-way handshake and PSH packets | TCP communication observed | `[Fig 11]` |
