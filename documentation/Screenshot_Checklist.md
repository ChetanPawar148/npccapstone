# Screenshot Evidence Checklist and Guide

**Student Name:** Chetan Pawar  
**PRN:** 2125UCSM1037  
**Course:** B.Tech Computer Science Engineering (Cyber Security)  
**Institution:** Sanjivani University, Kopargaon  
**Subject:** NPC Capstone Project  
**Academic Year:** 2026–2027  

---

## 1. Evidence Collection Guidelines

To maintain academic authenticity and forensic integrity:
1. **Genuine Evidence Only:** Capture all screenshots directly from your active laboratory virtual machine and hypervisor interface. Never fabricate, manipulate, or insert synthetic terminal outputs.
2. **Standard Image Format:** Save all screenshots as `.png` files inside `evidence/screenshots/`.
3. **Naming Convention:** Use the standardized filenames listed below (e.g., `fig01_vm_configuration.png`) to ensure seamless inclusion in the capstone report.

---

## 2. Master Screenshot Checklist

| Fig # | Screenshot Title & Caption | Suggested Filename | How to Capture | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Fig 01** | VM Hardware Specifications Dialog | `fig01_vm_configuration.png` | Open VMware/VirtualBox VM Settings dialog displaying RAM, vCPU, and Storage | `[Pending Lab Run]` |
| **Fig 02** | Network Adapter Isolation Settings | `fig02_network_isolation.png` | Snapshot of Network Adapter set to Disconnected or Host-Only | `[Pending Lab Run]` |
| **Fig 03** | Linux Guest Desktop & Boot Verification | `fig03_linux_guest_boot.png` | Clean Linux desktop/terminal open inside VM window | `[Pending Lab Run]` |
| **Fig 04** | Empirically Verified Internet Isolation | `fig04_internet_isolation_test.png`| Terminal running `ip route` and `ping -c 3 8.8.8.8` showing unreachable | `[Pending Lab Run]` |
| **Fig 05** | Clean Snapshot in Snapshot Manager | `fig05_clean_snapshot_manager.png`| Snapshot Manager showing `NPC_Capstone_Clean_State` | `[Pending Lab Run]` |
| **Fig 06** | Baseline Process & Socket Triage | `fig06_baseline_processes_ports.png`| Terminal showing `ps aux | head -n 20` and `ss -tulpn` before execution | `[Pending Lab Run]` |
| **Fig 07** | Safe Server Launch on Loopback | `fig07_server_launch.png` | Terminal 1 running `python3 server.py` displaying listening banner | `[Pending Lab Run]` |
| **Fig 08** | Listening Socket Verification (`ss`) | `fig08_listening_socket_ss.png` | Terminal 2 running `ss -tulpn | grep 54321` showing `127.0.0.1:54321` | `[Pending Lab Run]` |
| **Fig 09** | Safe Client Interaction (`STATUS`) | `fig09_client_interaction.png` | Terminal 3 running `python3 client.py` executing `STATUS` and `HELP` | `[Pending Lab Run]` |
| **Fig 10** | Active Process Triage During Run | `fig10_process_monitoring_ps.png` | Terminal running `ps -ef | grep server.py` showing PID and PPID | `[Pending Lab Run]` |
| **Fig 11** | Loopback Traffic Capture (`tcpdump`) | `fig11_loopback_pcap_tcpdump.png`| Terminal running `tcpdump -i lo port 54321` or Wireshark packet list | `[Pending Lab Run]` |
| **Fig 12** | File Identification & Attributes | `fig12_file_identification_stat.png`| Terminal running `ls -la server.py` and `file server.py` | `[Pending Lab Run]` |
| **Fig 13** | Cryptographic SHA-256 Calculation | `fig13_sha256_calculation.png` | Terminal running `sha256sum server.py client.py` | `[Pending Lab Run]` |
| **Fig 14** | VirusTotal Hash Lookup Results | `fig14_virustotal_hash_lookup.png` | Browser screenshot searching the SHA-256 hash on VirusTotal | `[Pending Lab Run]` |
| **Fig 15** | Snapshot Reversion to Clean State | `fig15_snapshot_restoration.png` | Snapshot Manager restoring to `NPC_Capstone_Clean_State` | `[Pending Lab Run]` |
| **Fig 16** | Post-Restoration Clean Audit | `fig16_post_restoration_audit.png`| Terminal running `ps aux | grep server.py` and `ss -tulpn` showing 0 traces | `[Pending Lab Run]` |

---

## 3. Step-by-Step Screenshot Capture Walkthrough

### Terminal Layout Tip (Split Screen)
For the most convincing evidence screenshots, you can arrange 2 or 3 terminal windows side-by-side:
- **Left Window:** Running `python3 server.py` (listener).
- **Middle Window:** Running `python3 client.py` (sending `STATUS`, `HELP`, `EXIT`).
- **Right Window:** Running `ss -tulpn | grep 54321` and `ps aux | grep server.py` (system triage).

This arrangement captures the entire client-server lifecycle in one view.
