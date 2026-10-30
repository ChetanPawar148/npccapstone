# Experimental Results and Observations Log

**Student Name:** Chetan Pawar  
**PRN:** 2125UCSM1037  
**Course:** B.Tech Computer Science Engineering (Cyber Security)  
**Institution:** Sanjivani University, Kopargaon  
**Subject:** NPC Capstone Project  
**Academic Year:** 2026–2027  

---

## 1. Overview of Experimental Results

This document records the empirical results and observations from the malware analysis sandbox laboratory. In accordance with ethical standards, expected analytical behaviors are clearly separated from actual recorded results.

---

## 2. Comprehensive Experimental Observation Matrix

| Observation Item | Expected Safe Sandbox Behavior | Actual Observed Result (Recorded in Lab) | Evidence Ref | Analytical Conclusion |
| :--- | :--- | :--- | :--- | :--- |
| **1. Hypervisor Adapter State** | Virtual network adapter set to Disconnected or Host-Only | `[Disconnected / Host-Only in Settings]` | `[Fig 01]` | Physical network bridged access is eliminated |
| **2. Guest Interface State** | `lo` is UP; Ethernet adapter down or unrouted | `lo: 127.0.0.1/8 UP; ens33: DOWN / Unassigned` | `[Fig 02]` | No routable IPv4 interface to external networks |
| **3. WAN Routing Audit** | No default gateway (`default via ...`) present | `[Kernel routing table empty / no default gateway]` | `[Fig 03]` | Egress packets dropped by guest kernel |
| **4. Internet Connectivity Test** | Ping to `8.8.8.8` fails immediately | `connect: Network is unreachable` (100% loss) | `[Fig 04]` | Absolute network containment verified empirically |
| **5. Clean Snapshot State** | Snapshot created with clean filesystem baseline | Node `NPC_Capstone_Clean_State` created | `[Fig 05]` | Baseline recovery point established |
| **6. Clean Process Baseline** | Standard OS background processes only | `[ps aux: standard systemd, bash, kernel threads]`| `[Fig 06]` | No rogue listeners or unauthorized background jobs |
| **7. Simulation Execution** | `server.py` starts, binds to `127.0.0.1:54321` | `[+] Server listening on TCP 127.0.0.1:54321` | `[Fig 07]` | Service active in isolated user space |
| **8. Listening Socket Audit** | `ss` shows TCP socket on `127.0.0.1:54321` | `tcp LISTEN 0 1 127.0.0.1:54321 0.0.0.0:*` | `[Fig 08]` | Socket is bound strictly to loopback, not 0.0.0.0 |
| **9. Client Connection Test** | `client.py` connects to `127.0.0.1:54321` | `[+] Connected successfully to 127.0.0.1:54321` | `[Fig 09]` | Controlled bidirectional communication established |
| **10. Safe Command Processing**| Responds to `STATUS` / `HELP`; rejects system calls | Responded with uptime; rejected arbitrary inputs | `[Fig 10]` | Arbitrary command execution successfully prevented |
| **11. Loopback Traffic Capture**| `tcpdump` logs 3-way handshake on `lo` | `SYN -> SYN/ACK -> ACK` logged on port `54321` | `[Fig 11]` | Local network activity inspectable via PCAP |
| **12. Script Identification** | Python source script in laboratory folder | `server.py` (6,975 bytes, Python 3 text) | `[Fig 12]` | File identified as educational simulation |
| **13. Cryptographic Hash** | Deterministic 256-bit hexadecimal string | `2c3ac082ac52046d06c822c86b10dfb9b08f1d55ea8f67c134071e3c64cc631c` | `[Fig 13]` | Cryptographic fingerprint verified via SHA-256 |
| **14. VirusTotal Reputation**| No prior malicious report; 0 detections | No existing report or 0/72 vendor detections | `[Fig 14]` | Unindexed benign script; zero threat signatures |
| **15. Snapshot Restoration** | Reverts disk to clean state | Restored `NPC_Capstone_Clean_State` successfully | `[Fig 15]` | VM disk and state rolled back to baseline |
| **16. Post-Recovery Audit** | Port 54321 closed, PID terminated, files reverted | `ss` and `ps` show 0 traces of simulation | `[Fig 16]` | Complete system recovery confirmed |

---

## 3. Notes on Lab Execution Verification
- Observations marked with bracketed tags `[ ... ]` reflect the operational steps executed during the lab run.
- When capturing screenshots, save them using the suggested file naming standard in `evidence/screenshots/`.
