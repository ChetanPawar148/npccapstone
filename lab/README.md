# Laboratory Directory

**Student:** Chetan Pawar  
**PRN:** 2125UCSM1037  
**Institution:** Sanjivani University, Kopargaon  
**Course:** B.Tech CSE (Cyber Security)  

---

## Laboratory Overview

This directory contains the laboratory code and experimental modules for the **NPC Capstone Project — Malware Analysis Sandbox Using VirtualBox or VMware**.

### Subdirectories and Components

1. **`safe_shell_simulation/`**:
   - `server.py`: Harmless, educational simulation of a bind-shell service listening exclusively on loopback (`127.0.0.1:54321`). Responds strictly to `STATUS`, `HELP`, and `EXIT`.
   - `client.py`: Harmless educational client for testing socket interaction with the local server.
   - `README.md`: Technical documentation explaining socket architecture, network isolation, execution procedures, and security safeguards.

### Laboratory Rules & Safety Guidelines
- All executions must remain strictly confined inside an isolated Linux virtual machine.
- Network adapters must be disconnected or set to host-only / isolated internal networking.
- No live weaponized malware or external remote command execution is permitted.
