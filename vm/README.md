# Virtual Machine Management & Safe Storage Notice

**Student Name:** Chetan Pawar  
**PRN:** 2125UCSM1037  
**Institution:** Sanjivani University, Kopargaon  
**Subject:** NPC Capstone Project  

---

## Virtual Machine Directory Guidelines

This directory provides operational notes and configuration guidelines for managing the VMware Workstation or VirtualBox virtual machine used in the malware sandbox capstone project.

### Critical Repository Safety Policies:
1. **NO Virtual Disk Commits:** Do **NOT** commit or upload large virtual disk files (`.vmdk`, `.vdi`, `.vhd`), RAM dumps (`.vmem`), or snapshot trees (`.vmsn`) to Git or GitHub. These files are typically 10 GB to 40 GB in size and violate GitHub's file size limits (maximum 100 MB per file).
2. **Git Ignore Protection:** The repository's `.gitignore` file is pre-configured to ignore all `.vmdk`, `.vdi`, `.iso`, and temporary hypervisor lock files automatically.
3. **VM Storage Best Practice:** Store the active virtual machine disk on local host storage (e.g., `C:\Virtual Machines\Linux_Malware_Sandbox\`) outside the synced Git working tree.
