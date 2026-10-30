# NPC Capstone Project: Malware Analysis Sandbox Using VirtualBox or VMware

[![Academic Project](https://img.shields.io/badge/Academic%20Year-2026--2027-blue.svg)](#student-information)
[![Department](https://img.shields.io/badge/Department-CSE%20Cyber%20Security-navy.svg)](#student-information)
[![Status](https://img.shields.io/badge/Laboratory%20Status-Documented%20%26%20Instrumented-success.svg)](#experimental-workflow)
[![Report](https://img.shields.io/badge/Report-PDF%20Available-orange.svg)](report/NPC_Capstone_Malware_Analysis_Sandbox_Report.pdf)

> **Official Capstone Project Deliverable**  
> **Student Name:** Chetan Pawar  
> **PRN:** 2125UCSM1037  
> **Degree:** Bachelor of Technology (B.Tech) in Computer Science Engineering  
> **Specialization:** Cyber Security  
> **Institution:** Sanjivani University, Kopargaon  
> **Subject:** NPC Capstone Project  

---

## 📄 Capstone Project Report

The complete, university-formatted academic PDF report is compiled and available in this repository:

👉 **[Download the Capstone Project Report](report/NPC_Capstone_Malware_Analysis_Sandbox_Report.pdf)** (39 KB, 14 Pages, well below the university 10 MB limit)  
👉 **[View Editable Report Source Markdown](report/report_source.md)**

---

## 🎯 Assignment Objectives & Scope

Dynamic malware analysis necessitates executing untrusted code within a strictly controlled, non-destructive virtual environment. This project demonstrates:
1. **Hypervisor Virtual Machine Hardening:** Provisioning an isolated Ubuntu Linux guest inside VMware Workstation or Oracle VM VirtualBox.
2. **Empirical Network Isolation:** Enforcing and validating zero Internet/WAN access via interface audits, routing checks, and reachability tests.
3. **Clean State Snapshot Generation:** Establishing a baseline recovery point labeled `NPC_Capstone_Clean_State` prior to testing.
4. **Harmless Bind-Shell Simulation:** Developing and executing a benign client-server demonstration confined strictly to loopback (`127.0.0.1:54321`) that processes harmless whitelist commands (`STATUS`, `HELP`, `EXIT`) and prevents arbitrary command execution.
5. **Multi-Vector System Monitoring:** Tracing live processes (`ps`, `top`), socket bindings (`ss`), open handles (`lsof`), loopback packets (`tcpdump`), and file modifications (`stat`).
6. **Cryptographic Identification & Threat Intelligence:** Calculating deterministic SHA-256 digests and performing responsible, privacy-preserving reputation queries on VirusTotal.
7. **Snapshot Restoration & Verification:** Restoring the VM to `NPC_Capstone_Clean_State` and auditing the operating system to confirm complete eradication of all runtime artifacts.

---

## 🏗️ Laboratory Architecture & Hardware Profile

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

### Provisioning Specifications

| Component | Minimum Specification | Recommended Specification | Configured Value |
| :--- | :--- | :--- | :--- |
| **Hypervisor** | VirtualBox 7.x or VMware 16.x | VMware Workstation Pro / Player 17.x | VMware Workstation Pro / VirtualBox |
| **Guest OS** | Ubuntu 20.04 LTS | Ubuntu 22.04 LTS (64-bit) | Ubuntu 22.04 LTS |
| **Processors** | 1 vCPU | 2 vCPUs | 2 vCPUs |
| **Memory (RAM)**| 2048 MB (2 GB) | 4096 MB (4 GB) | 4096 MB |
| **Virtual Disk**| 20 GB | 30 GB – 40 GB (Dynamically Allocated) | 30.0 GB |
| **Network Adapter** | 1 Virtual NIC | Disconnected or Host-Only (No WAN) | Disconnected / Host-Only |
| **Shared Folders**| Disabled | Disabled | Disabled |

---

## 🔒 Network Isolation Strategy & Verification

A malware sandbox must never rely on assumptions. Isolation is established and empirically verified:

1. **Adapter Isolation:** The virtual network adapter is set to **Disconnected** (Cable Unplugged) or mapped to an isolated private switch without default gateway routing.
2. **Empirical Guest Verification:**
   - `ip addr show`: Confirms `lo` is UP on `127.0.0.1/8`; physical Ethernet adapters (`ens33`/`enp0s3`) are unassigned or down.
   - `ip route show`: Confirms no default gateway (`default via ...`) is present.
   - `ping -c 3 8.8.8.8`: Fails immediately with `connect: Network is unreachable`.
   - `curl -I --connect-timeout 5 https://www.google.com`: Fails with resolution or connection error.

---

## 📸 Clean Snapshot Baseline: `NPC_Capstone_Clean_State`

Before any experimental code is introduced or executed:
1. Boot the clean guest VM.
2. Audit baseline processes (`ps aux > baseline_processes.txt`) and listening ports (`ss -tulpn > baseline_ports.txt`).
3. Take a clean snapshot in VMware or VirtualBox with the designated label:
   ```
   NPC_Capstone_Clean_State
   ```
4. Verify the snapshot node appears in the hypervisor Snapshot Manager.

---

## 🛡️ Safe Educational Bind-Shell Simulation

To study socket binding and process triage ethically without weaponized code:

- **Loopback Enforcement:** Binds exclusively to `127.0.0.1:54321`. External adapters cannot reach this service.
- **Whitelist Input Handling:** Responds strictly to `STATUS`, `HELP`, and `EXIT`.
- **Zero OS Command Execution:** Contains NO `os.system()`, `subprocess.Popen()`, `exec()`, or `/bin/sh` shell invocations. Arbitrary shell commands are caught and rejected.
- **Components:**
  - `lab/safe_shell_simulation/server.py`: Harmless educational bind-shell simulation server.
  - `lab/safe_shell_simulation/client.py`: Harmless test client connecting locally.
  - `lab/safe_shell_simulation/README.md`: Architectural documentation and execution guide.

---

## 🔍 System Monitoring Toolkit

| Utility | Command Syntax | What It Reveals in Sandbox Triage |
| :--- | :--- | :--- |
| **`ps`** | `ps aux \| grep server.py` | Process ID (PID), user security context, memory footprint, command-line arguments |
| **`top`** | `top -b -n 1` | Real-time CPU and memory consumption confirming absence of runaway loops |
| **`ss`** | `ss -tulpn \| grep 54321` | Protocol (`tcp`), socket state (`LISTEN`), local address (`127.0.0.1:54321`), PID |
| **`lsof`** | `lsof -p <PID>` | Open file descriptors including standard streams (`/dev/pts/X`) and TCP socket handle |
| **`tcpdump`**| `sudo tcpdump -i lo port 54321` | Captures TCP 3-way handshake, PSH-ACK application messages, and FIN-ACK teardown |
| **`stat`** | `stat server.py` | Exact file size (6,975 bytes), inode number, and timestamps (atime, mtime, ctime) |
| **`sha256sum`**| `sha256sum server.py client.py`| Computes deterministic cryptographic hashes for immutable file identification |

---

## 🔐 Cryptographic Hashing & VirusTotal Findings

### Calculated File Fingerprints

| File Name | File Size | MD5 Digest | SHA-256 Digest |
| :--- | :--- | :--- | :--- |
| **`server.py`** | 6,975 bytes | `d4d96fc789a35b6e7d9e1d8550e13bd9` | `2c3ac082ac52046d06c822c86b10dfb9b08f1d55ea8f67c134071e3c64cc631c` |
| **`client.py`** | 2,872 bytes | `221b49ef872dc7705cbc1400d55ce518` | `e5724b85bf68128adb31f7af4abd38bf07fd1d8cda3aa07cf3f89ae71fc79993` |

### VirusTotal Threat Intelligence Investigation
- **Query Method:** Passive SHA-256 hash lookup (No files uploaded, preserving student privacy).
- **Official Assignment Status Statement:**
  > **"No existing VirusTotal report was available for the investigated file at the time of analysis."**
- **Evaluation:** As an educational script created locally in an isolated lab, the sample has not been indexed publicly. A clean or unindexed result does not prove safety; static signature reputation must always be supplemented with dynamic behavioral observation.

---

## 🔄 Snapshot Restoration & Before-and-After Comparison

### Restoration Procedure:
1. Power down the virtual machine.
2. In VMware or VirtualBox Snapshot Manager, select `NPC_Capstone_Clean_State` and click **Restore / Go To**.
3. Boot the restored VM.
4. Execute verification audits:
   - `ps aux | grep server.py` ➔ No processes found.
   - `ss -tulpn | grep 54321` ➔ No active listening sockets.
   - Temporary files in `/tmp` generated during runtime are completely eradicated.

### Forensic Comparison Matrix

| Parameter | 1. Clean Baseline Snapshot | 2. During Active Experiment | 3. Post-Restoration State |
| :--- | :--- | :--- | :--- |
| **Virtual Disk State** | Clean OS | Modified (scripts, logs, PCAPs) | Clean OS (Reverted) |
| **Process Table** | Standard system daemons only | `python3 server.py` active | Standard system daemons only |
| **Port 54321** | Closed / Unbound | `LISTEN` on `127.0.0.1` | Closed / Unbound |
| **Loopback TCP Sockets** | None | `ESTABLISHED` connection | None |
| **Temporary Files** | Clean `/tmp` | Execution logs & PCAP buffers | Clean `/tmp` (Discarded) |

---

## ⚠️ Critical Forensic Limitations of Snapshots

1. **Shared Folders Non-Reversion:** Files modified on the host machine through shared folders are **NOT** reverted when guest snapshots are restored.
2. **External Storage Contamination:** USB drives or external network drives mounted during analysis retain any modifications permanently.
3. **Hypervisor Evasion & VM Escapes:** Advanced malware may exploit device driver vulnerabilities to break out of guest ring 0 into host memory.
4. **Anti-Sandbox Evasion:** Malware may detect virtualization artifacts (vendor MAC addresses, low CPU cores, lack of mouse movement) and remain dormant.
5. **Non-Reversible Network Actions:** Outbound network transmissions cannot be undone by reverting a local snapshot.

---

## 📁 Repository Directory Structure

```
NPC_Capstone_Malware_Analysis_Sandbox/
|
|-- README.md                                          <- Project overview and documentation
|-- .gitignore                                         <- Prevents committing VM disks & memory dumps
|-- generate_pdf.py                                    <- Automated ReportLab PDF generator script
|
|-- report/
|   |-- NPC_Capstone_Malware_Analysis_Sandbox_Report.pdf <- Formal academic report (<10 MB)
|   |-- report_source.md                               <- Full editable markdown source
|
|-- documentation/
|   |-- Lab_Setup_Guide.md                             <- VM hardware specs and setup instructions
|   |-- Network_Isolation_Guide.md                     <- Network modes, loopback dynamics & verification
|   |-- Snapshot_Recovery_Guide.md                     <- Clean snapshot creation and restoration
|   |-- Monitoring_Guide.md                            <- Linux triage commands (ps, ss, lsof, top)
|   |-- VirusTotal_Analysis_Guide.md                   <- Threat intelligence methodology & privacy
|   |-- Results_and_Observations.md                    <- Structured experimental observation log
|   |-- Screenshot_Checklist.md                        <- 16-point screenshot evidence checklist
|
|-- lab/
|   |-- README.md                                      <- Laboratory overview
|   |-- safe_shell_simulation/
|       |-- README.md                                  <- Socket architecture and safe usage
|       |-- server.py                                  <- Safe loopback bind-shell simulation
|       |-- client.py                                  <- Safe local test client
|
|-- evidence/
|   |-- README.md                                      <- Evidence directory policies
|   |-- screenshots/                                   <- Place genuine .png screenshots here
|   |-- logs/                                          <- Baseline & runtime triage outputs
|   |-- packet_captures/                               <- tcpdump PCAP loopback capture files
|
|-- analysis/
|   |-- File_Identification.md                         <- Static attributes and MIME classifications
|   |-- Hash_Results.md                                <- MD5, SHA-1, and SHA-256 cryptographic digests
|   |-- VirusTotal_Findings.md                         <- Threat intelligence analysis & VT findings
|
|-- references/
|   |-- References.md                                  <- Official technical citations & standards
|
|-- vm/
|   |-- README.md                                      <- Virtual machine storage and safety notes
```

---

## 📸 Master Screenshot Evidence Checklist

| Figure | Evidence Description | Suggested Filename | Location |
| :---: | :--- | :--- | :--- |
| **Fig 01** | VM Hardware Specifications Dialog | `fig01_vm_configuration.png` | `evidence/screenshots/` |
| **Fig 02** | Network Adapter Isolation Settings | `fig02_network_isolation.png` | `evidence/screenshots/` |
| **Fig 03** | Linux Guest Desktop & Boot Verification | `fig03_linux_guest_boot.png` | `evidence/screenshots/` |
| **Fig 04** | Empirically Verified Internet Isolation | `fig04_internet_isolation_test.png`| `evidence/screenshots/` |
| **Fig 05** | Clean Snapshot in Snapshot Manager | `fig05_clean_snapshot_manager.png`| `evidence/screenshots/` |
| **Fig 06** | Baseline Process & Socket Triage | `fig06_baseline_processes_ports.png`| `evidence/screenshots/` |
| **Fig 07** | Safe Server Launch on Loopback | `fig07_server_launch.png` | `evidence/screenshots/` |
| **Fig 08** | Listening Socket Verification (`ss`) | `fig08_listening_socket_ss.png` | `evidence/screenshots/` |
| **Fig 09** | Safe Client Interaction (`STATUS`) | `fig09_client_interaction.png` | `evidence/screenshots/` |
| **Fig 10** | Active Process Triage During Run | `fig10_process_monitoring_ps.png` | `evidence/screenshots/` |
| **Fig 11** | Loopback Traffic Capture (`tcpdump`) | `fig11_loopback_pcap_tcpdump.png`| `evidence/screenshots/` |
| **Fig 12** | File Identification & Attributes | `fig12_file_identification_stat.png`| `evidence/screenshots/` |
| **Fig 13** | Cryptographic SHA-256 Calculation | `fig13_sha256_calculation.png` | `evidence/screenshots/` |
| **Fig 14** | VirusTotal Hash Lookup Results | `fig14_virustotal_hash_lookup.png` | `evidence/screenshots/` |
| **Fig 15** | Snapshot Reversion to Clean State | `fig15_snapshot_restoration.png` | `evidence/screenshots/` |
| **Fig 16** | Post-Restoration Clean Audit | `fig16_post_restoration_audit.png`| `evidence/screenshots/` |

---

## 📚 References & Standards

1. Oracle Corporation. (2024). *Oracle VM VirtualBox User Manual: Virtual Networking and Snapshots*. [Oracle Docs](https://docs.oracle.com/en/virtualization/virtualbox/)
2. VMware / Broadcom. (2024). *VMware Workstation Pro Documentation: Virtual Networking*. [VMware Docs](https://docs.vmware.com/en/VMware-Workstation-Pro/)
3. NIST. (2013). *Guide to Malware Incident Prevention and Handling*. NIST SP 800-83 Rev. 1.
4. M. Sikorski and A. Honig. (2012). *Practical Malware Analysis*. No Starch Press.
5. R. Braden. (1989). *RFC 1122: Requirements for Internet Hosts (Loopback Addresses)*. IETF.
6. VirusTotal / Google Chronicle. (2024). *VirusTotal Threat Intelligence Documentation*. [VirusTotal Docs](https://docs.virustotal.com/)
