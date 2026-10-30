# Virtual Machine Snapshot Creation and Recovery Guide

**Student Name:** Chetan Pawar  
**PRN:** 2125UCSM1037  
**Course:** B.Tech Computer Science Engineering (Cyber Security)  
**Institution:** Sanjivani University, Kopargaon  
**Subject:** NPC Capstone Project  
**Academic Year:** 2026–2027  

---

## 1. The Role of Snapshots in Malware Sandboxing

A **virtual machine snapshot** freezes the state of a virtual machine at a specific instant in time, including:
1. Virtual disk state (file system, installed binaries, system libraries).
2. Virtual RAM and CPU execution registers (if snapshot is taken while VM is running).
3. Hypervisor hardware configuration settings.

In malware analysis, snapshots serve as the fundamental recovery mechanism. Because malicious binaries frequently modify system binaries, register persistent startup entries, drop droppers into `/tmp` or `C:\Windows\System32`, and tamper with security controls, a clean snapshot allows an investigator to return the virtual disk to a known clean, uncontaminated state in seconds.

---

## 2. Snapshot Naming and Baseline Preparation

### Designated Clean Snapshot Name:
```
NPC_Capstone_Clean_State
```

### Mandatory Pre-Snapshot Checklist:
Before taking the clean snapshot, verify that:
- [ ] Operating system is freshly booted and all core updates are complete.
- [ ] Analysis tools (Python 3, `ss`, `ip`, `ps`, `tcpdump` if available) are pre-installed.
- [ ] Network adapter is set to **Host-Only**, **Internal**, or **Disconnected** (as per the Isolation Guide).
- [ ] Internet unreachability is verified with `ping` and `curl`.
- [ ] No experimental scripts, malware samples, or test logs exist in `/home` or `/tmp`.
- [ ] Baseline process table is captured (`ps aux > baseline_processes.txt`).
- [ ] Baseline listening ports are captured (`ss -tulpn > baseline_ports.txt`).

---

## 3. Creating the Clean Snapshot (`NPC_Capstone_Clean_State`)

### Procedure in VMware Workstation (GUI)
1. Power off the Linux VM gracefully (recommended for a smaller, pristine disk snapshot) or pause at the clean desktop.
2. In the top menu, navigate to **VM** > **Snapshot** > **Take Snapshot...**.
3. In the dialog window:
   - **Name:** `NPC_Capstone_Clean_State`
   - **Description:** `Clean, uninfected baseline state for NPC Capstone sandbox. Network isolated, no background listeners, pristine filesystem.`
4. Click **Take Snapshot**.
5. Open the Snapshot Manager (**VM** > **Snapshot** > **Snapshot Manager...**) to confirm the node `NPC_Capstone_Clean_State` is visible directly beneath the root.

### Procedure in VMware Workstation (CLI via `vmrun`)
```bash
# Power off the VM cleanly
"C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe" stop "path\to\your_vm.vmx" soft

# Create the clean snapshot
"C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe" snapshot "path\to\your_vm.vmx" "NPC_Capstone_Clean_State"

# Verify snapshot existence
"C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe" listSnapshots "path\to\your_vm.vmx"
```

### Procedure in Oracle VirtualBox (GUI)
1. In the VirtualBox Manager, select the Linux virtual machine.
2. In the right panel, switch from **Details** to **Snapshots** (or click the hamburger menu > **Snapshots**).
3. Click the **Take** button (camera icon).
4. Enter:
   - **Name:** `NPC_Capstone_Clean_State`
   - **Description:** `Clean isolated baseline state for NPC Capstone experiment.`
5. Click **OK**.

### Procedure in Oracle VirtualBox (CLI via `VBoxManage`)
```bash
VBoxManage snapshot "Linux_Malware_Sandbox" take "NPC_Capstone_Clean_State" --description "Clean baseline state"
VBoxManage snapshot "Linux_Malware_Sandbox" list
```

---

## 4. Restoring the Virtual Machine to Clean State

Once the controlled simulation or dynamic malware analysis run is completed, the sandbox must be restored.

### Procedure in VMware Workstation
1. Shut down or power off the experimental virtual machine.
2. Navigate to **VM** > **Snapshot** > **Snapshot Manager...**.
3. Select `NPC_Capstone_Clean_State` from the snapshot tree.
4. Click **Go To** (or **Revert**).
5. A warning dialog will appear: *"Going to this snapshot will cause the current state of the virtual machine to be discarded."* Click **Yes**.
6. Power on the VM.

### Procedure in Oracle VirtualBox
1. Close the VM window and select **Power off the machine**, checking **Restore current snapshot 'NPC_Capstone_Clean_State'**; OR
2. In the VirtualBox Manager, select the VM, go to the **Snapshots** tab, select `NPC_Capstone_Clean_State`, and click **Restore**.

---

## 5. Post-Restoration Verification & Integrity Audit

After powering on the restored VM, perform empirical checks to confirm that experimental artifacts have been successfully eliminated:

### Verification Commands:

```bash
# 1. Verify that the simulation process is NOT running
ps aux | grep -E "server.py|client.py" | grep -v grep
# Expected: Empty output (No processes found)

# 2. Verify that port 54321 is NOT listening
ss -tulpn | grep 54321
# Expected: Empty output (No socket open)

# 3. Check for experimental scripts in test directories
ls -la /tmp/ /home/*/lab/
# Expected: Experimental test files created during analysis are absent
```

---

## 6. Before-and-After Forensic Comparison

| Parameter / State | Baseline (Clean Snapshot) | During Experiment | Post-Restoration State |
| :--- | :--- | :--- | :--- |
| **Virtual Disk State** | Pristine OS filesystem | Modified (test scripts, logs, PCAPs) | Reverted to identical baseline hash |
| **Process Table** | Standard OS daemons only | `python3 server.py`, `python3 client.py` | Standard OS daemons only |
| **Listening Ports** | No test ports open | TCP `127.0.0.1:54321` active | No test ports open |
| **Active TCP Sockets** | No local loopback connections | Active `ESTABLISHED` socket | No local loopback connections |
| **Temporary Files** | Clean `/tmp` directory | Logs and PCAPs generated in `/tmp` | `/tmp` reverted to baseline state |

---

## 7. Critical Forensic Limitations of Snapshots

While snapshots provide reliable disk and memory rollback within the virtual container, security analysts must understand their boundaries:

1. **Shared Folders Vulnerability:** If hypervisor Shared Folders are enabled, changes made to files on the host filesystem or network shares **ARE NOT REVERTED** when the VM snapshot is restored.
2. **External Storage / USB Passthrough:** If a physical USB drive or external network volume was attached to the VM during execution, any file modifications or malware droppers written to that external device remain permanent.
3. **Hypervisor / Host Integrity:** In rare advanced persistent threat (APT) scenarios involving hypervisor vulnerabilities (VM escape exploits), malicious code escaping from guest ring 0 to host ring 0 will persist on the host operating system regardless of guest snapshot reversion.
4. **Non-Reversible Network Actions:** If network isolation was breached and malware sent packets to external servers, snapshot reversion cannot undo the data exfiltration or notifications received by the remote attacker.
