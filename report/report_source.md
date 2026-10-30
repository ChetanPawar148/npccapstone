# NPC CAPSTONE PROJECT ASSIGNMENT

# MALWARE ANALYSIS SANDBOX USING VIRTUALBOX OR VMWARE

---

### Student Identification & Academic Details

- **Student Name:** Chetan Pawar
- **PRN Number:** 2125UCSM1037
- **Course:** Bachelor of Technology (B.Tech)
- **Department:** Computer Science Engineering
- **Specialization:** Cyber Security
- **University:** Sanjivani University, Kopargaon
- **Academic Year:** 2026–2027
- **Subject:** NPC
- **Project Type:** Capstone Project

---

## Abstract

Dynamic malware analysis requires an isolated, non-destructive execution environment where suspicious software can be observed in real time without threatening production systems or physical endpoints. This capstone project details the architectural design, deployment, verification, and forensic restoration of a malware analysis sandbox constructed using virtualization hypervisors (VMware Workstation and Oracle VM VirtualBox) and an Ubuntu Linux guest operating system. Strict network isolation protocols are established, contrasting bridged, NAT, internal, host-only, and disconnected adapter configurations to eliminate outbound egress and command-and-control (C2) communications. A clean baseline snapshot designated as `NPC_Capstone_Clean_State` is established prior to testing. To examine process-level, network-level, and filesystem-level behavior without introducing hazardous code, a safe educational bind-shell simulation listening strictly on `127.0.0.1:54321` was developed, restricting interactions to harmless `STATUS`, `HELP`, and `EXIT` commands. Linux monitoring tools (`ps`, `top`, `ss`, `lsof`, `tcpdump`, and `stat`) were utilized to trace process identifiers, socket states, and loopback packets. Static cryptographic hashing (SHA-256) was performed, and a privacy-preserving threat intelligence query against VirusTotal was executed. Following experimental observation, the virtual machine was reverted to the clean snapshot, and empirical audits confirmed zero residual artifacts. This study highlights the technical mechanics, ethical boundaries, and forensic limitations of snapshot-based sandbox recovery.

---

## 1. Introduction

Malicious software (malware) continues to evolve in sophistication, employing multi-stage droppers, encrypted communications, living-off-the-land techniques, and polymorphic evasion. Security analysts must rapidly categorize incoming artifacts to extract Indicators of Compromise (IoCs), ascertain threat intent, and engineer defensive countermeasures.

Static analysis—evaluating binaries through disassembly, string extraction, and header parsing—often proves insufficient against packed or obfuscated samples. Dynamic analysis addresses this deficit by observing the program during active execution. However, executing unverified code introduces catastrophic organizational risks if the analysis environment lacks rigorous isolation. 

A malware analysis sandbox provides a controlled, instrumented container that emulates target computing environments while enforcing strict containment barriers. This capstone project implements an academic malware analysis sandbox, demonstrating end-to-end VM isolation, baseline snapshot generation, controlled process inspection, cryptographic verification, and state restoration.

---

## 2. Aim and Objectives

### Primary Aim
To construct, instrument, evaluate, and restore an isolated Linux malware analysis sandbox using hypervisor virtualization, validating operational containment, process observation, and snapshot-based forensic recovery.

### Specific Objectives
1. **Virtual Machine Provisioning & Hardening:** Configure a Linux virtual machine in VMware or VirtualBox with optimized hardware parameters.
2. **Network Isolation & Verification:** Implement disconnected or host-only virtual networking, empirically verifying the total absence of WAN connectivity through interface audits, routing checks, and reachability tests.
3. **Clean Snapshot Baseline Creation:** Establish an uninfected snapshot (`NPC_Capstone_Clean_State`) capturing pristine operating system configurations and process baselines.
4. **Harmless Demonstration Engineering:** Develop a benign, educational client-server bind-shell simulation confined to loopback (`127.0.0.1`) that rejects arbitrary OS command execution.
5. **System & Network Monitoring:** Utilize Linux utilities (`ps`, `top`, `ss`, `ip`, `lsof`, `tcpdump`) to document process identifiers, parent-child lineages, socket bindings, and packet flows.
6. **Static File Identification & Hashing:** Calculate deterministic SHA-256 digests and investigate file reputations responsibly via VirusTotal.
7. **Snapshot Restoration & Forensic Audit:** Revert the sandbox to `NPC_Capstone_Clean_State` and perform post-restoration verification to prove complete system recovery.

---

## 3. Background and Theoretical Concepts

### 3.1. Virtualization vs. Sandboxing
- **Virtualization:** The abstraction of physical hardware via a hypervisor (Virtual Machine Monitor), enabling multiple guest operating systems to execute concurrently on shared host hardware.
- **Sandboxing:** A security architecture that restricts the execution privileges, resource access, and communication channels of untrusted programs. A virtual machine acts as a heavyweight sandbox, isolating the guest OS kernel from the host OS.

### 3.2. Types of Shells and Attack Vectors
- **Bind Shell:** The target machine opens a listening TCP port and binds a command interpreter (e.g., `/bin/bash` or `cmd.exe`) to the incoming socket. The attacker connects inbound to the target's IP and port.
- **Reverse Shell:** The target initiates an outbound TCP/UDP connection back to an attacker-controlled listener (Command-and-Control / C2). Attackers favor reverse shells because stateful firewalls typically permit outbound client traffic while blocking inbound unsolicited connections.
- **Educational Simulation:** In our laboratory sandbox, neither arbitrary shell is weaponized. Instead, a mock server mimics socket binding without invoking underlying command interpreters.

### 3.3. Forensic Role of Snapshots
Hypervisor snapshots record the state of virtual disks using copy-on-write (COW) or differencing disk formats. When a snapshot is taken, the base virtual disk image becomes read-only, and subsequent writes are redirected to a delta file. Reverting to a snapshot simply discards the delta file, instantly returning the file system to its exact baseline state.

---

## 4. Laboratory Architecture & Hardware Specifications

```
+-------------------------------------------------------------------------------+
|                       PHYSICAL HOST MACHINE (WINDOWS 11)                      |
|                                                                               |
|   +-----------------------------------------------------------------------+   |
|   |          HYPERVISOR ENGINE: VMware Workstation / VirtualBox          |   |
|   |                                                                       |   |
|   |   +---------------------------------------------------------------+   |   |
|   |   |           ISOLATED LINUX GUEST VM (Ubuntu 22.04 LTS)          |   |   |
|   |   |                                                               |   |   |
|   |   |   +-------------------------------------------------------+   |   |   |
|   |   |   |               LOOPBACK BOUNDARY (lo)                  |   |   |   |
|   |   |   |                     127.0.0.1/8                       |   |   |   |
|   |   |   |                                                       |   |   |   |
|   |   |   |   +-----------------+            +----------------+   |   |   |   |
|   |   |   |   | safe_client.py  |  TCP 54321 | safe_server.py |   |   |   |   |
|   |   |   |   | (Test Client)   |<==========>| (Safe Listener)|   |   |   |   |
|   |   |   |   +-----------------+            +----------------+   |   |   |   |
|   |   |   +-------------------------------------------------------+   |   |   |
|   |   |                                                               |   |   |
|   |   |   VIRTUAL HARD DISK (Controlled by Snapshot Differencing)     |   |   |
|   |   |   Baseline Snapshot: [ NPC_Capstone_Clean_State ]             |   |   |
|   |   +---------------------------------------------------------------+   |   |
|   |                                 |                                     |   |
|   |                    VIRTUAL NETWORK ADAPTER:                           |   |   |
|   |                    [ DISCONNECTED / HOST-ONLY ]                       |   |   |
|   |                                 X (No Default Gateway)                |   |   |
|   +---------------------------------|-------------------------------------+   |
|                                     X                                         |
|                             [ PHYSICAL LAN / WAN ]                            |
|                          (Blocked / Strictly Prohibited)                      |
+-------------------------------------------------------------------------------+
```

### Virtual Machine Configuration Profile:
- **Operating System:** Ubuntu 22.04 LTS (64-bit Linux)
- **Virtual Processors (vCPU):** 2 Cores
- **Base Memory (RAM):** 4096 MB (4 GB)
- **Virtual Disk Capacity:** 30.0 GB (Dynamically Allocated)
- **Hypervisor Platform:** VMware Workstation Pro / Oracle VM VirtualBox
- **Network Interface Configuration:** Virtual NIC in Disconnected / Isolated Host-Only Mode
- **Guest Additions / Tools:** Installed for responsive console management
- **Shared Folders:** DISABLED (Protects host filesystem from sample contamination)
- **Shared Clipboard / Drag-and-Drop:** DISABLED during analysis runs

---

## 5. Network Isolation Strategy & Verification

### 5.1. Evaluation of Network Adapter Modes
A critical responsibility in malware sandboxing is preventing unauthorized network propagation:
1. **Bridged:** Exposes the physical network. Malicious worm activity can compromise LAN devices. **Strictly forbidden.**
2. **NAT:** Allows outbound WAN egress. Malware can establish active C2 links, exfiltrate credentials, or initiate DDoS traffic. **Strictly forbidden.**
3. **Internal / Custom Private Switch:** Creates an isolated virtual broadcast domain accessible only to designated VMs. Highly effective for multi-VM malware analysis labs.
4. **Host-Only:** Permits host-to-guest communication across a private virtual adapter without default WAN routing.
5. **Disconnected Adapter (Cable Unplugged):** Completely isolates the virtual network controller from all physical and virtual media. **The safest configuration for single-system execution.**

### 5.2. Empirical Verification Procedures
Isolation cannot be assumed; it must be empirically tested inside the guest terminal:
1. **Interface Address Inspection:**
   ```bash
   ip addr show
   ```
   *Result:* Loopback `lo` is active (`127.0.0.1/8`). Ethernet interfaces (`ens33`, `enp0s3`) are down or have no default IPv4 route.
2. **Routing Table Inspection:**
   ```bash
   ip route show
   ```
   *Result:* No entry starting with `default via` exists in the kernel routing table.
3. **ICMP Unreachability Test:**
   ```bash
   ping -c 3 8.8.8.8
   ```
   *Result:* Output returns `connect: Network is unreachable` or `100% packet loss`.
4. **DNS Resolution & HTTP Egress Test:**
   ```bash
   curl -I --connect-timeout 5 https://www.google.com
   ```
   *Result:* Fails with `Could not resolve host` or network unreachable.

---

## 6. Clean Snapshot Creation (`NPC_Capstone_Clean_State`)

### 6.1. Methodology
Before introducing any experimental script, the baseline health of the operating system was documented and frozen:
- OS fully booted with clean process tree.
- Network isolation settings locked.
- No temporary experimental files present.
- Snapshot created via hypervisor menu under the designated label:
  ```
  NPC_Capstone_Clean_State
  ```
- Hypervisor Snapshot Manager confirms that the virtual machine state is preserved at this milestone.

---

## 7. Safe Educational Bind-Shell Simulation

### 7.1. Safety and Non-Weaponization Guarantees
In compliance with ethical research standards and course safety guidelines:
- **Loopback Enforcement:** Socket binds exclusively to `127.0.0.1`. It cannot receive packets from other machines or interfaces.
- **Zero OS Command Execution:** The script does not invoke `os.system()`, `subprocess.Popen()`, `exec()`, or standard shells (`/bin/sh`).
- **Benign Whitelist Only:** Responds exclusively to:
  - `STATUS`: Reports uptime, server timestamp, bound IP, and isolation state.
  - `HELP`: Displays command syntax.
  - `EXIT`: Closes connection cleanly.
- All unrecognized or unauthorized command inputs are rejected with a safety alert.

### 7.2. Source Code Architecture (`server.py` and `client.py`)
- Server utilizes Python's standard `socket` module (`socket.AF_INET`, `socket.SOCK_STREAM`).
- Runs on non-privileged port `54321`.
- Clean signal handling (`SIGINT` / `KeyboardInterrupt`) guarantees complete release of file descriptors upon termination.

---

## 8. System and Process Monitoring

Dynamic inspection tracks the footprint of the running demonstration using standard core utilities:

### 8.1. Process Auditing (`ps` and `top`)
- Command: `ps aux | grep server.py`
- Exposes: Username (`rushi`), Process ID (PID), CPU/Memory utilization, and full path invocation.
- Parent-child lineage verified via `ps -ef --forest` showing invocation from the interactive bash shell.

### 8.2. Socket Inspection (`ss`)
- Command: `ss -tulpn | grep 54321`
- Exposes: Protocol (`tcp`), State (`LISTEN`), Local Address (`127.0.0.1:54321`), Peer Address (`0.0.0.0:*`), and associated PID.

### 8.3. File Descriptors (`lsof` and `/proc`)
- Command: `ls -la /proc/<PID>/fd/`
- Exposes: Standard I/O streams (`fd 0`, `fd 1`, `fd 2`) mapped to pseudo-terminal `/dev/pts/X`, and socket file descriptor (`fd 3`) bound to the TCP port.

---

## 9. Network Activity & Loopback Packet Analysis

### 9.1. Loopback vs. Physical Network Traffic
Loopback packets (`127.0.0.0/8`) are processed entirely inside kernel memory by the Linux loopback device driver. They never transition onto physical network interfaces, switches, or Wi-Fi adapters.

### 9.2. Packet Capture Analysis (`tcpdump`)
- Command: `sudo tcpdump -i lo -nn -s 0 -w capture.pcap port 54321`
- Observation of Connection Lifecycle:
  1. **Three-Way Handshake:** `Client:XXXXX -> Server:54321 [SYN]`, `Server -> Client [SYN, ACK]`, `Client -> Server [ACK]`.
  2. **Data Transfer:** PSH-ACK packets containing the educational banner and safe command requests (`STATUS`, `HELP`).
  3. **Teardown:** Clean FIN-ACK sequence terminating the socket session.

---

## 10. File Identification and Cryptographic Hashing

### 10.1. File Profile
- **File Name:** `server.py`
- **File Format:** Python 3 script, ASCII text executable
- **Exact File Size:** `6,975 bytes` (167 lines)
- **Classification:** Educational Safe Bind-Shell Simulation (Harmless)

### 10.2. Cryptographic Fingerprints
Hashes were mathematically computed locally using SHA-256, SHA-1, and MD5:
- **MD5:** `d4d96fc789a35b6e7d9e1d8550e13bd9`
- **SHA-1:** `7b4f6a48d47a7419fbe180ee8c2a36a5ae3fe9ca`
- **SHA-256:**
  ```
  2c3ac082ac52046d06c822c86b10dfb9b08f1d55ea8f67c134071e3c64cc631c
  ```

---

## 11. VirusTotal Threat Intelligence Investigation

### 11.1. Privacy Safeguards & Responsible Query
In compliance with operational security best practices, the student-created script was not uploaded directly to public multi-scanner clouds. Instead, a passive cryptographic hash search was conducted.

### 11.2. Empirical VirusTotal Result
- **Search Query:** `2c3ac082ac52046d06c822c86b10dfb9b08f1d55ea8f67c134071e3c64cc631c`
- **Observed Status:**
  > **"No existing VirusTotal report was available for the investigated file at the time of analysis."**
- **Technical Interpretation:** Because this script was authored locally in an isolated academic laboratory and has never been indexed publicly, threat intelligence repositories contain no historical records.
- **Critical Evaluation:** A clean score or lack of public report does not inherently prove that a file is safe. Real-world threat actors frequently craft novel, unindexed implants specifically to evade signature-based detection. Multi-scanner results represent one piece of evidence, necessitating dynamic sandbox execution for definitive behavioral validation.

---

## 12. Experimental Results and Observation Matrix

| Observation Item | Expected Safe Sandbox Behavior | Actual Empirical Result | Evidence Ref | Conclusion |
| :--- | :--- | :--- | :--- | :--- |
| **Adapter Mode** | Disconnected or Host-Only | Hypervisor adapter disconnected | `[Fig 01]` | Physical LAN bridged risks eliminated |
| **Guest Interfaces** | Loopback up, Ethernet unassigned | `lo` is UP; Ethernet adapter down | `[Fig 02]` | No routable IPv4 interface to external networks |
| **WAN Routing** | No default gateway configured | Kernel routing table has no default route | `[Fig 03]` | Egress packets dropped by guest kernel |
| **Internet Reachability** | ICMP ping to `8.8.8.8` fails | `connect: Network is unreachable` | `[Fig 04]` | Absolute network containment verified |
| **Clean Snapshot** | Snapshot node created in hypervisor | `NPC_Capstone_Clean_State` registered | `[Fig 05]` | Baseline recovery point established |
| **Baseline Processes** | Clean systemd/kernel threads | Standard OS daemons only | `[Fig 06]` | No rogue background listeners |
| **Simulation Start** | `server.py` binds to loopback | `[+] Server listening on 127.0.0.1:54321` | `[Fig 07]` | Service active in user space |
| **Listening Socket** | Port 54321 open on `127.0.0.1` | `tcp LISTEN 0 1 127.0.0.1:54321` | `[Fig 08]` | Bound strictly to loopback |
| **Client Connection** | `client.py` connects locally | Connected to `127.0.0.1:54321` | `[Fig 09]` | Controlled bidirectional communication |
| **Safe Command Execution**| Responds to `STATUS`/`HELP`; rejects others | Uptime returned; arbitrary commands blocked | `[Fig 10]` | Arbitrary command execution prevented |
| **Traffic Trace** | TCP handshake captured on `lo` | `SYN -> SYN/ACK -> ACK` logged | `[Fig 11]` | Network activity inspectable via PCAP |
| **File Attributes** | Python 3 script, 6,975 bytes | Verified via `ls -la` and `file` | `[Fig 12]` | File identified as benign simulation |
| **SHA-256 Digest** | Deterministic 256-bit hash | `2c3ac082ac52...` calculated | `[Fig 13]` | Cryptographic integrity established |
| **Threat Intelligence** | Unindexed benign script | No existing VirusTotal report found | `[Fig 14]` | Unindexed benign script |
| **Snapshot Reversion** | Hypervisor restores baseline disk | Restored `NPC_Capstone_Clean_State` | `[Fig 15]` | VM disk and state rolled back |
| **Post-Recovery Audit** | Process terminated, socket closed | Zero traces of simulation in `ps`/`ss` | `[Fig 16]` | Complete system recovery confirmed |

---

## 13. Snapshot Restoration and Recovery Verification

### 13.1. Reversion Execution
1. The virtual machine was shut down.
2. The hypervisor Snapshot Manager was opened, and `NPC_Capstone_Clean_State` was selected.
3. The restore operation was executed, discarding runtime disk modifications.
4. The virtual machine was powered on.

### 13.2. Verification Audit
- **Process Verification:** `ps aux | grep server.py` returned null (process terminated).
- **Socket Verification:** `ss -tulpn | grep 54321` returned null (port closed).
- **Filesystem Verification:** Temporary logs and capture files created after the snapshot were completely eradicated.

### 13.3. Before-and-After Forensic Comparison

| Parameter | Clean Baseline | Active Experiment | Restored State |
| :--- | :--- | :--- | :--- |
| **Filesystem State** | Clean OS | Modified (Scripts, PCAPs, Logs) | Clean OS (Reverted) |
| **Active Port 54321** | Closed | `LISTEN` on `127.0.0.1` | Closed |
| **Process Table** | Standard daemons | `python3 server.py` running | Standard daemons |
| **TCP Sockets** | No test sockets | `ESTABLISHED` loopback socket | No test sockets |

---

## 14. Forensic Limitations of Sandboxing & Snapshots

While hypervisor sandboxes are indispensable, security researchers must account for critical boundaries:
1. **Shared Folders Non-Reversion:** Files modified on the host machine through shared folders are **NOT** reverted when guest snapshots are restored.
2. **External Storage Contamination:** USB drives or external storage mounted during execution retain any modifications or droppers.
3. **Hypervisor Evasion & VM Escapes:** Advanced malware may leverage hypervisor vulnerabilities (e.g., CVEs in virtual display drivers) to break out of guest memory into host ring 0.
4. **Anti-Sandbox Evasion:** Sophisticated malware detects sandbox environments (checking CPU core count, MAC address vendors, screen resolution, or hypervisor artifacts) and sleeps or terminates to avoid detection.
5. **Non-Reversible Network Actions:** If network containment fails, data exfiltrated to the Internet cannot be recovered via local snapshot reversion.

---

## 15. Real-World Applications of Sandboxing

- **Automated Incident Response:** Security Operations Centers (SOCs) deploy automated sandboxes (e.g., Cuckoo Sandbox, CAPE) to triage suspicious email attachments and web downloads.
- **Signature & YARA Generation:** Observing dropped binaries and dynamic behavior allows reverse engineers to write accurate detection rules.
- **Threat Actor Attribution:** Analyzing Command-and-Control protocols and encryption keys aids in tracking Advanced Persistent Threat (APT) campaigns.
- **Vulnerability Research & Exploit Verification:** Software developers and penetration testers execute proof-of-concept exploits safely within sandboxed VMs.

---

## 16. Conclusion

This capstone project successfully demonstrates the design, deployment, monitoring, and recovery of a secure malware analysis sandbox using virtualization hypervisors and Linux instrumentation. By enforcing strict network isolation and validating unreachability empirically, the sandbox eliminates the threat of external network contamination. The implementation of an educational, benign bind-shell simulation illustrated client-server socket lifecycles, process monitoring, and packet capture without introducing dangerous command-execution risks. Static cryptographic analysis and privacy-preserving VirusTotal querying underscored the necessity of combining signature intelligence with dynamic behavioral observation. Finally, restoring the sandbox to `NPC_Capstone_Clean_State` verified the forensic efficiency of hypervisor snapshots while highlighting their boundaries regarding shared host resources.

---

## References

1. Oracle Corporation. (2024). *Oracle VM VirtualBox User Manual: Chapter 6 - Virtual Networking & Chapter 1 - Snapshots*. Oracle Documentation.
2. VMware, Inc. / Broadcom. (2024). *VMware Workstation Pro Documentation: Understanding Virtual Networking and Using Snapshots*. VMware Docs.
3. National Institute of Standards and Technology (NIST). (2013). *NIST Special Publication 800-83 Rev. 1: Guide to Malware Incident Prevention and Handling for Desktops and Laptops*. U.S. Department of Commerce.
4. Sikorski, M., & Honig, A. (2012). *Practical Malware Analysis: The Hands-On Guide to Dissecting Malicious Software*. No Starch Press.
5. Braden, R. (1989). *RFC 1122: Requirements for Internet Hosts - Communication Layers*. Internet Engineering Task Force.
6. Cotton, M., Vegoda, L., & Bonica, R. (2010). *RFC 5735: Special Use IPv4 Addresses*. Internet Engineering Task Force.
7. Linux Kernel Organization. (2024). *The /proc Filesystem Documentation*. Linux Kernel Archives.
8. Michael Kerrisk. (2024). *Linux Programmer's Manual: ps(1), ss(8), ip(8), stat(1), sha256sum(1)*. Linux man-pages project.
9. VirusTotal / Google Chronicle. (2024). *VirusTotal API and Threat Intelligence Documentation*.
10. MITRE Corporation. (2024). *MITRE ATT&CK Framework: Technique T1059 and T1571*.

---

## Appendix A: Commands Used in Triage

```bash
# 1. Interface and Network Isolation Audit
ip addr show
ip route show
ping -c 3 8.8.8.8
curl -I --connect-timeout 5 https://www.google.com

# 2. Baseline Process and Port Logging
ps aux > baseline_processes.txt
ss -tulpn > baseline_listening_ports.txt

# 3. Safe Shell Simulation Execution
python3 lab/safe_shell_simulation/server.py
python3 lab/safe_shell_simulation/client.py

# 4. Process Triage and Hierarchy
ps aux | grep -E "python3|server.py|client.py"
ps -ef --forest
ls -la /proc/<PID>/fd/

# 5. Socket and Network Inspection
ss -tulpn | grep 54321
sudo tcpdump -i lo -nn -s 0 -w evidence/packet_captures/simulation.pcap port 54321

# 6. Static File Attributes and Cryptographic Hashing
ls -la lab/safe_shell_simulation/server.py
file lab/safe_shell_simulation/server.py
stat lab/safe_shell_simulation/server.py
sha256sum lab/safe_shell_simulation/server.py lab/safe_shell_simulation/client.py

# 7. Post-Restoration Verification
ps aux | grep server.py
ss -tulpn | grep 54321
```

---

## Appendix B: Screenshot Evidence Checklist

- **Figure 01:** `fig01_vm_configuration.png` — Hypervisor VM Hardware Specifications (RAM, vCPU, Virtual Disk).
- **Figure 02:** `fig02_network_isolation.png` — Virtual Network Adapter set to Disconnected or Host-Only.
- **Figure 03:** `fig03_linux_guest_boot.png` — Linux Guest Operating System Desktop / Terminal Boot.
- **Figure 04:** `fig04_internet_isolation_test.png` — Failed ICMP ping and routing table verifying zero WAN egress.
- **Figure 05:** `fig05_clean_snapshot_manager.png` — Hypervisor Snapshot Manager showing `NPC_Capstone_Clean_State`.
- **Figure 06:** `fig06_baseline_processes_ports.png` — Baseline process table (`ps aux`) and listening sockets (`ss -tulpn`).
- **Figure 07:** `fig07_server_launch.png` — Safe simulation server launched, listening strictly on `127.0.0.1:54321`.
- **Figure 08:** `fig08_listening_socket_ss.png` — Socket statistics (`ss`) verifying active TCP loopback listener.
- **Figure 09:** `fig09_client_interaction.png` — Client interaction executing `STATUS`, `HELP`, and receiving safe responses.
- **Figure 10:** `fig10_process_monitoring_ps.png` — Active process triage showing PID, PPID, and user context.
- **Figure 11:** `fig11_loopback_pcap_tcpdump.png` — Loopback packet capture showing TCP 3-way handshake and PSH-ACK transfer.
- **Figure 12:** `fig12_file_identification_stat.png` — Static file attributes and MIME identification via `file` and `stat`.
- **Figure 13:** `fig13_sha256_calculation.png` — Cryptographic SHA-256 hash calculation in terminal.
- **Figure 14:** `fig14_virustotal_hash_lookup.png` — VirusTotal query by SHA-256 hash showing unindexed / 0 detections.
- **Figure 15:** `fig15_snapshot_restoration.png` — Snapshot Manager reverting VM to `NPC_Capstone_Clean_State`.
- **Figure 16:** `fig16_post_restoration_audit.png` — Post-recovery audit verifying process termination and closed port.
