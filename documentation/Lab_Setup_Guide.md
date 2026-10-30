# Laboratory Setup Guide: Malware Analysis Sandbox

**Student Name:** Chetan Pawar  
**PRN:** 2125UCSM1037  
**Course:** B.Tech Computer Science Engineering (Cyber Security)  
**Institution:** Sanjivani University, Kopargaon  
**Subject:** NPC Capstone Project  
**Academic Year:** 2026–2027  

---

## 1. Laboratory Objective

The primary objective of this laboratory is to establish a secure, fully isolated virtualization sandbox using **VirtualBox** or **VMware Workstation** for dynamic malware analysis and behavior observation. By strictly decoupling the guest virtual machine (VM) from the physical host network and the Internet, security analysts can safely inspect suspicious binaries, monitor process execution, record network socket activity, and observe system state modifications without endangering organizational infrastructure or physical endpoints.

---

## 2. Hardware and Virtual Machine Specifications

To ensure smooth analysis while maintaining adequate host performance, the guest virtual machine should be provisioned with the following recommended specifications:

| Hardware Component | Minimum Requirement | Recommended Specification | Rationale |
| :--- | :--- | :--- | :--- |
| **Hypervisor** | VirtualBox 7.x or VMware Workstation 16/17 | VMware Workstation Pro / Player 17.x or VirtualBox 7.0 | Robust snapshot management and networking controls |
| **Guest OS** | Ubuntu 22.04 LTS Desktop / Server | Ubuntu 22.04 / 24.04 LTS Desktop | Standard Linux distribution with comprehensive monitoring utilities |
| **Virtual CPUs (vCPU)** | 1 Core | 2 Cores | Prevents thread starvation during concurrent process tracing |
| **RAM** | 2048 MB (2 GB) | 4096 MB (4 GB) | Sufficient memory for operating system, utilities, and packet capture buffers |
| **Virtual Disk Space** | 20 GB | 30 GB – 40 GB (Dynamically Allocated) | Ample storage for OS, dependencies, log storage, and swap |
| **Display Memory** | 32 MB | 128 MB (with 3D Acceleration optional) | Responsive terminal and GUI desktop experience |
| **Network Adapter** | 1 Virtual NIC | 1 Virtual NIC set to **Host-Only** or **Disconnected** | Strict containment preventing outbound WAN communication |

---

## 3. Network Configuration Modes Comparison

Selecting the appropriate hypervisor network adapter mode is the cornerstone of malware sandbox isolation. The five standard modes behave as follows:

```
+----------------------------------------------------------------------------------------------------+
|                                    HYPERVISOR NETWORK MODES                                        |
+--------------------+------------------------------------+------------------+-----------------------+
| Network Mode       | Guest-to-Host Communication        | Host-to-Guest    | Internet (WAN) Access |
+--------------------+------------------------------------+------------------+-----------------------+
| 1. Bridged         | Yes (shares physical LAN)          | Yes              | YES (High Risk)       |
| 2. NAT             | Outbound via host translation     | Port-forward only| YES (High Risk)       |
| 3. Host-Only       | Yes (isolated private subnet)      | Yes (private IP) | NO (Unless bridged)   |
| 4. Internal (VBox) | No (VM-to-VM private only)         | No               | NO                    |
| 5. Disconnected    | NO (Cable Unplugged / Disabled)    | NO               | NO (Safest Mode)      |
+--------------------+------------------------------------+------------------+-----------------------+
```

### Detailed Evaluation of Modes:
1. **Bridged Networking:**
   - *How it works:* The guest VM appears as a distinct physical machine on the host's physical network, receiving an IP address directly from the local LAN DHCP router.
   - *Security Risk:* **EXTREMELY HAZARDOUS for malware analysis.** Malicious traffic or worm-like replication can infect the physical host and other devices on the LAN.
2. **NAT (Network Address Translation):**
   - *How it works:* The hypervisor translates VM requests using the host IP address. Outbound traffic reaches the Internet, but inbound unsolicited connections are blocked.
   - *Security Risk:* **HAZARDOUS for malware analysis.** Live malware can contact external Command-and-Control (C2) servers, exfiltrate data, or participate in DDoS attacks.
3. **Host-Only Networking:**
   - *How it works:* Creates an isolated virtual switch (`vmnet1` in VMware, `vboxnet0` in VirtualBox) shared exclusively between the host and virtual machines. No physical default gateway is attached to the Internet.
   - *Suitability:* Acceptable for monitored inter-VM labs, provided host adapters are not bridged to WAN.
4. **Internal Networking (VirtualBox) / Custom VMnet (VMware):**
   - *How it works:* Confined completely within hypervisor memory. Only VMs assigned to the identical internal network name can communicate. The host operating system cannot even ping the VM.
   - *Suitability:* Excellent for multi-node isolated analysis (e.g., REMnux fake C2 + Windows victim).
5. **Disconnected Adapter (Cable Unplugged / No Adapter):**
   - *How it works:* The virtual network adapter is logically powered off, unmapped, or has its virtual link cable disconnected (`linkstate=off`).
   - *Suitability:* **THE SAFEST PRACTICAL CONFIGURATION** for standalone single-VM behavior observation and script analysis.

---

## 4. Step-by-Step Isolation Setup

### Option A: VMware Workstation Procedure
1. Power off the Linux VM.
2. Right-click the VM in the library and select **Settings...**.
3. Under the **Hardware** tab, select **Network Adapter**.
4. In the right-hand pane, choose either:
   - **Custom (VMnet2 - VMnet19):** An isolated private virtual switch with NO DHCP/NAT connected to the host physical interface; OR
   - Deselect **Connected** and **Connect at power on** (Cable Unplugged).
5. Click **OK** to save settings.
6. Under **Options** > **Shared Folders**, ensure Shared Folders are set to **Disabled** to prevent VM escapes or malware writing to the host filesystem.

### Option B: Oracle VirtualBox Procedure
1. Power off the Linux VM.
2. Click **Settings** (gear icon) > **Network**.
3. Under **Adapter 1**, ensure the **Attached to:** dropdown is set to:
   - **Internal Network** (named `MalwareLabNet`); OR
   - **Not Attached**; OR
   - Check **Enable Network Adapter**, set to **Host-only Adapter**, expand **Advanced**, and uncheck **Cable Connected**.
4. Under **General** > **Advanced**, set **Shared Clipboard** to **Disabled** and **Drag'n'Drop** to **Disabled**.
5. Click **OK**.

---

## 5. Verification of Complete Network Isolation

Never assume a sandbox is isolated merely because hypervisor settings were adjusted. You must verify isolation empirically from inside the Linux guest terminal before executing any test.

### Step 1: Inspect Assigned IP Addresses
Execute in the Linux VM terminal:
```bash
ip addr show
```
*Expected Result:*
- The loopback interface `lo` displays `127.0.0.1/8` with state `UP`.
- Ethernet interfaces (e.g., `ens33`, `enp0s3`, or `eth0`) are either missing an IPv4 address, show state `DOWN`, or display only an isolated non-routable link-local address (`169.254.x.x`).

### Step 2: Inspect the Kernel Routing Table
Execute:
```bash
ip route show
```
*Expected Result:*
- No default gateway (`default via X.X.X.X`) should appear.
- If an isolated host-only subnet exists, only local subnet routes should be visible.

### Step 3: Test ICMP Internet Ping by IP
Test direct numeric connectivity to bypass DNS:
```bash
ping -c 3 8.8.8.8
```
*Expected Empirical Result:*
```
connect: Network is unreachable
# OR
3 packets transmitted, 0 received, 100% packet loss, time 2048ms
```

### Step 4: Test Domain Resolution & HTTP Connectivity
Attempt an outbound web request:
```bash
curl -I --connect-timeout 5 https://www.google.com
```
*Expected Empirical Result:*
```
curl: (6) Could not resolve host: www.google.com
# OR
curl: (7) Failed to connect to www.google.com: Network is unreachable
```

### Step 5: Document Isolation Evidence
Capture screenshots showing:
1. Hypervisor Network Settings dialog showing Disconnected / Host-Only / Internal configuration.
2. Terminal output showing `ip addr show`, `ip route show`, and failed ping/curl attempts.
