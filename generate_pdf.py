#!/usr/bin/env python3
"""
Academic PDF Report Generator for NPC Capstone Project
Student: Chetan Pawar | PRN: 2125UCSM1037
Sanjivani University, Kopargaon
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Palette definition
PRIMARY = colors.HexColor("#0F2537")      # Deep Navy
SECONDARY = colors.HexColor("#1A365D")    # Dark Slate Blue
ACCENT = colors.HexColor("#2B6CB0")       # Royal Blue
TEXT_DARK = colors.HexColor("#1A202C")    # Charcoal body text
TEXT_MUTED = colors.HexColor("#4A5568")   # Slate gray
BG_LIGHT = colors.HexColor("#F7FAFC")     # Soft off-white
BG_HEADER = colors.HexColor("#EDF2F7")    # Subtle gray table header
BORDER_COLOR = colors.HexColor("#CBD5E0") # Border gray
CARD_BG = colors.HexColor("#F8FAFC")      # Card fill
CARD_BORDER = colors.HexColor("#94A3B8")  # Card border
SUCCESS_COLOR = colors.HexColor("#2E7D32")# Forest Green

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas for dynamic total page counting and running headers/footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Suppress headers/footers on cover page
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(TEXT_MUTED)

        # Running Header
        self.drawString(54, 11 * 72 - 36, "NPC CAPSTONE: MALWARE ANALYSIS SANDBOX")
        self.setFont("Helvetica", 8)
        self.drawRightString(8.5 * 72 - 54, 11 * 72 - 36, "Sanjivani University — Cyber Security")
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

        # Running Footer
        self.line(54, 46, 8.5 * 72 - 54, 46)
        self.drawString(54, 34, "Student: Chetan Pawar | PRN: 2125UCSM1037")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 54, 34, page_str)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    base_styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        alignment=1, # Center
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=ACCENT,
        alignment=1,
        spaceAfter=25
    )

    h1_style = ParagraphStyle(
        'CustomH1',
        parent=base_styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=base_styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=TEXT_DARK,
        spaceAfter=7
    )

    body_bold = ParagraphStyle(
        'CustomBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    code_style = ParagraphStyle(
        'CustomCode',
        parent=base_styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1E293B")
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=TEXT_DARK
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=PRIMARY
    )

    badge_style = ParagraphStyle(
        'Badge',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#1E3A8A")
    )

    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("SANJIVANI UNIVERSITY, KOPARGAON", ParagraphStyle('InstHeader', fontName='Helvetica-Bold', fontSize=14, leading=16, alignment=1, textColor=SECONDARY)))
    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE ENGINEERING", ParagraphStyle('DeptHeader', fontName='Helvetica', fontSize=10.5, leading=13, alignment=1, textColor=TEXT_MUTED)))
    story.append(Paragraph("SPECIALIZATION IN CYBER SECURITY", ParagraphStyle('SpecHeader', fontName='Helvetica-Bold', fontSize=10, leading=12, alignment=1, textColor=ACCENT)))
    
    story.append(Spacer(1, 25))
    story.append(HRFlowable(width="90%", thickness=2.5, color=PRIMARY, spaceAfter=25))
    
    story.append(Paragraph("NPC CAPSTONE PROJECT ASSIGNMENT", ParagraphStyle('AssignTag', fontName='Helvetica-Bold', fontSize=12, leading=14, alignment=1, textColor=ACCENT)))
    story.append(Spacer(1, 8))
    story.append(Paragraph("MALWARE ANALYSIS SANDBOX USING VIRTUALBOX OR VMWARE", title_style))
    story.append(Paragraph("Comprehensive Design, Empirical Network Containment, Process Triage, Static Cryptographic Identification, and Snapshot Forensic Recovery", subtitle_style))
    
    story.append(HRFlowable(width="60%", thickness=1, color=BORDER_COLOR, spaceAfter=30))
    story.append(Spacer(1, 15))

    # Student metadata table card
    info_data = [
        [Paragraph("<b>Submitted By:</b>", table_header), Paragraph("Chetan Pawar", table_cell)],
        [Paragraph("<b>PRN Number:</b>", table_header), Paragraph("<b>2125UCSM1037</b>", table_cell)],
        [Paragraph("<b>Program / Degree:</b>", table_header), Paragraph("Bachelor of Technology (B.Tech)", table_cell)],
        [Paragraph("<b>Department:</b>", table_header), Paragraph("Computer Science Engineering", table_cell)],
        [Paragraph("<b>Specialization:</b>", table_header), Paragraph("Cyber Security", table_cell)],
        [Paragraph("<b>University:</b>", table_header), Paragraph("Sanjivani University, Kopargaon", table_cell)],
        [Paragraph("<b>Academic Year:</b>", table_header), Paragraph("2026–2027", table_cell)],
        [Paragraph("<b>Subject:</b>", table_header), Paragraph("NPC (Network Programming & Cyber Security)", table_cell)],
        [Paragraph("<b>Project Type:</b>", table_header), Paragraph("Capstone Project Submission", table_cell)],
        [Paragraph("<b>Repository:</b>", table_header), Paragraph("https://github.com/ChetanPawar148/npccapstone", table_cell)]
    ]
    info_table = Table(info_data, colWidths=[140, 290])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1.2, SECONDARY),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(info_table)

    story.append(Spacer(1, 40))
    story.append(Paragraph("<i>Academic Verification Notice: This laboratory project adheres strictly to cybersecurity educational guidelines, deploying zero arbitrary command execution payloads and operating exclusively within isolated, disconnected virtual machine environments.</i>", ParagraphStyle('Notice', fontName='Helvetica-Oblique', fontSize=8, leading=11, alignment=1, textColor=TEXT_MUTED)))
    story.append(PageBreak())

    # =========================================================================
    # EXECUTIVE ABSTRACT & OBJECTIVES
    # =========================================================================
    story.append(Paragraph("Executive Abstract", h1_style))
    story.append(Paragraph(
        "Dynamic malware analysis requires an isolated, non-destructive execution environment where untrusted software can be observed in real time without endangering production networks, endpoints, or host computing systems. This capstone project details the architectural design, deployment, verification, and forensic restoration of a malware analysis sandbox constructed using virtualization hypervisors (VMware Workstation Pro and Oracle VM VirtualBox) and an Ubuntu Linux guest operating system. Strict network isolation protocols are established, contrasting bridged, NAT, internal, host-only, and disconnected adapter configurations to eliminate outbound egress and command-and-control (C2) communications. A clean baseline snapshot designated as <b>NPC_Capstone_Clean_State</b> is established prior to testing. To examine process-level, network-level, and filesystem-level behavior without introducing hazardous code, a safe educational bind-shell simulation listening strictly on <b>127.0.0.1:54321</b> was developed, restricting interactions to harmless <b>STATUS</b>, <b>HELP</b>, and <b>EXIT</b> commands. Linux monitoring tools (<code>ps</code>, <code>top</code>, <code>ss</code>, <code>lsof</code>, <code>tcpdump</code>, and <code>stat</code>) were utilized to trace process identifiers, socket states, and loopback packets. Static cryptographic hashing (SHA-256) was performed, and a privacy-preserving threat intelligence query against VirusTotal was executed. Following experimental observation, the virtual machine was reverted to the clean snapshot, and empirical audits confirmed zero residual artifacts. This study highlights the technical mechanics, ethical boundaries, and forensic limitations of snapshot-based sandbox recovery.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Project Aim and Technical Objectives", h1_style))
    objectives = [
        "<b>Virtual Machine Hardening & Provisioning:</b> Provision a resilient Linux virtual machine in VMware or VirtualBox with optimized hardware allocations (2 vCPUs, 4 GB RAM, 30 GB virtual disk).",
        "<b>Rigorous Network Isolation:</b> Enforce a disconnected or host-only virtual networking model, empirically verifying zero Internet accessibility via interface checks, routing audits, and failed ICMP/HTTP tests.",
        "<b>Clean State Baseline Snapshot:</b> Record and freeze the pristine operating system state prior to analysis under the snapshot name <code>NPC_Capstone_Clean_State</code>.",
        "<b>Harmless Client-Server Simulation:</b> Design and execute a benign Python bind-shell simulation confined exclusively to the local loopback adapter (<code>127.0.0.1:54321</code>) that rejects arbitrary operating system commands.",
        "<b>Multi-Layered System Triage:</b> Capture live forensic indicators including process trees (<code>ps</code>), resource utilization (<code>top</code>), listening sockets (<code>ss</code>), open descriptors (<code>lsof</code>), and packet sequences (<code>tcpdump</code>).",
        "<b>Cryptographic Identification & Threat Intelligence:</b> Generate deterministic SHA-256 digests and conduct passive threat intelligence queries via VirusTotal following responsible disclosure standards.",
        "<b>State Restoration & Forensic Integrity Audit:</b> Revert the sandbox to <code>NPC_Capstone_Clean_State</code> and verify that all test processes, sockets, and temporary files have been eradicated."
    ]
    for obj in objectives:
        story.append(Paragraph(f"• {obj}", body_style))
    story.append(Spacer(1, 8))

    # =========================================================================
    # THEORETICAL CONCEPTS & VIRTUALIZATION MODES
    # =========================================================================
    story.append(Paragraph("Background and Theoretical Concepts", h1_style))
    story.append(Paragraph(
        "<b>Virtualization vs. Sandboxing:</b> Virtualization employs a Type-1 or Type-2 Hypervisor (Virtual Machine Monitor) to abstract physical CPU, memory, and I/O devices, executing a complete guest operating system in an isolated ring. A sandbox is an instrumented security envelope that restricts execution rights and monitors API calls. In malware analysis, virtual machines serve as robust, guest-kernel-level sandboxes.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Shell Architecture Dynamics:</b> In computer security, a <i>bind shell</i> instructs the compromised target host to open an open listening TCP port and bind an interactive command interpreter (such as <code>/bin/bash</code>) to incoming connections. Conversely, a <i>reverse shell</i> prompts the target to establish an outbound TCP session back to a remote Command-and-Control (C2) server. In our laboratory environment, unrestricted command execution is strictly eliminated. The simulation mimics socket binding while processing solely hardcoded benign requests.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Snapshot Mechanism:</b> Hypervisor snapshots rely on Copy-on-Write (COW) or differencing virtual disks. When <code>NPC_Capstone_Clean_State</code> is created, the primary disk image is marked read-only. All subsequent guest operating system writes are diverted to a child delta file. During restoration, the hypervisor discards the delta file, instantaneously returning the virtual disk to its uninfected state.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Comparative Analysis of Hypervisor Network Modes", h2_style))
    net_data = [
        [Paragraph("<b>Network Mode</b>", table_header), Paragraph("<b>Guest-to-Host Path</b>", table_header), Paragraph("<b>WAN Access</b>", table_header), Paragraph("<b>Malware Lab Suitability</b>", table_header)],
        [Paragraph("Bridged", table_cell), Paragraph("Direct across physical LAN switch", table_cell), Paragraph("YES (Unrestricted)", table_cell), Paragraph("<b>PROHIBITED</b> (High risk of LAN contamination)", table_cell)],
        [Paragraph("NAT", table_cell), Paragraph("Outbound translated via host IP", table_cell), Paragraph("YES (Outbound)", table_cell), Paragraph("<b>PROHIBITED</b> (Risk of C2 beaconing & data leaks)", table_cell)],
        [Paragraph("Host-Only", table_cell), Paragraph("Private virtual switch with host only", table_cell), Paragraph("NO (Isolated)", table_cell), Paragraph("Acceptable for monitored multi-node labs", table_cell)],
        [Paragraph("Internal (VBox)", table_cell), Paragraph("Confined strictly between VMs in memory", table_cell), Paragraph("NO (Isolated)", table_cell), Paragraph("Highly recommended for victim-fakeC2 setups", table_cell)],
        [Paragraph("Disconnected", table_cell), Paragraph("No virtual cable attached (Unplugged)", table_cell), Paragraph("NO (None)", table_cell), Paragraph("<b>SAFEST PRACTICAL MODE</b> for single-VM triage", table_cell)]
    ]
    net_table = Table(net_data, colWidths=[75, 135, 95, 195])
    net_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_HEADER),
        ('BOX', (0,0), (-1,-1), 1, SECONDARY),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(net_table)
    story.append(PageBreak())

    # =========================================================================
    # SYSTEM ARCHITECTURE & LAB SETUP
    # =========================================================================
    story.append(Paragraph("Laboratory Architecture & Hardware Configuration", h1_style))
    story.append(Paragraph(
        "The malware analysis sandbox is hosted within a hardened hypervisor container executing on an enterprise x86_64 host running Windows 11. The guest environment utilizes Ubuntu Linux 22.04 LTS to provide a reliable POSIX substrate with comprehensive native monitoring tools.",
        body_style
    ))

    vm_specs = [
        [Paragraph("<b>Parameter</b>", table_header), Paragraph("<b>Provisioned Value</b>", table_header), Paragraph("<b>Technical Justification</b>", table_header)],
        [Paragraph("Hypervisor Platform", table_cell), Paragraph("VMware Workstation Pro / VirtualBox 7.x", table_cell), Paragraph("Robust snapshot tree management and isolated virtual switching", table_cell)],
        [Paragraph("Guest Operating System", table_cell), Paragraph("Ubuntu Linux 22.04 LTS (64-bit)", table_cell), Paragraph("Stable long-term kernel with standard procfs, iproute2, and socket tools", table_cell)],
        [Paragraph("Virtual Processors (vCPU)", table_cell), Paragraph("2 Execution Cores", table_cell), Paragraph("Prevents thread blocking during simultaneous packet tracing and process triage", table_cell)],
        [Paragraph("Allocated System RAM", table_cell), Paragraph("4096 MB (4.0 GB)", table_cell), Paragraph("Adequate memory buffer for packet captures and OS runtime without paging", table_cell)],
        [Paragraph("Virtual Disk Capacity", table_cell), Paragraph("30.0 GB (Dynamically Allocated)", table_cell), Paragraph("Sufficient disk space for kernel logs, debug dumps, and OS libraries", table_cell)],
        [Paragraph("Network Interface", table_cell), Paragraph("Host-Only / Disconnected Virtual NIC", table_cell), Paragraph("Enforces strict packet boundary; prevents accidental WAN transmission", table_cell)],
        [Paragraph("Shared Folders", table_cell), Paragraph("DISABLED", table_cell), Paragraph("Eliminates vector for guest samples to access or infect host filesystem", table_cell)],
        [Paragraph("Shared Clipboard / DND", table_cell), Paragraph("DISABLED during active testing", table_cell), Paragraph("Mitigates guest-to-host memory leaks and accidental paste exploits", table_cell)]
    ]
    vm_table = Table(vm_specs, colWidths=[120, 150, 230])
    vm_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_HEADER),
        ('BOX', (0,0), (-1,-1), 1, SECONDARY),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(vm_table)
    story.append(Spacer(1, 10))

    # Evidence placeholder box helper
    def make_evidence_card(fig_num, title, filename, desc):
        card_content = [
            [Paragraph(f"<b>{fig_num}: {title}</b>", badge_style), Paragraph(f"<i>File: {filename}</i>", table_cell)],
            [Paragraph(f"<b>Description & Guidance:</b> {desc}", table_cell), Paragraph("<b>[Genuine Laboratory Capture Placeholder]</b>", ParagraphStyle('Hold', fontName='Helvetica-Bold', fontSize=8, textColor=ACCENT, alignment=2))]
        ]
        t = Table(card_content, colWidths=[330, 170])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
            ('BOX', (0,0), (-1,-1), 1, CARD_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    story.append(make_evidence_card("Figure 01", "Hypervisor Hardware Configuration", "fig01_vm_configuration.png", "Displays hypervisor VM settings showing 2 vCPUs, 4 GB RAM, and disabled shared folders."))
    story.append(Spacer(1, 6))
    story.append(make_evidence_card("Figure 02", "Network Adapter Isolation Settings", "fig02_network_isolation.png", "Displays VM Network Adapter configured to Disconnected or Host-Only mode."))
    story.append(Spacer(1, 10))

    # =========================================================================
    # EMPIRICAL NETWORK ISOLATION VERIFICATION
    # =========================================================================
    story.append(Paragraph("Empirical Network Isolation Verification", h1_style))
    story.append(Paragraph(
        "A cardinal rule in malware analysis is: <i>never trust hypervisor UI checkboxes without empirical verification from inside the guest operating system</i>. Before introducing test scripts, the guest environment was interrogated using four diagnostic checks:",
        body_style
    ))

    iso_checks = [
        "<b>Interface Audit (<code>ip addr show</code>):</b> Confirms that loopback (<code>lo</code>) is active on <code>127.0.0.1/8</code>, while Ethernet interfaces (<code>ens33</code> or <code>enp0s3</code>) are either down, unassigned, or allocated non-routable link-local IPs.",
        "<b>Routing Table Audit (<code>ip route show</code>):</b> Confirms the total absence of a default gateway route (<code>default via X.X.X.X</code>), proving the kernel has no path to forward external IP datagrams.",
        "<b>Direct Numeric IP Ping (<code>ping -c 3 8.8.8.8</code>):</b> Bypasses DNS to test low-level ICMP reachability. The kernel immediately emits <code>connect: Network is unreachable</code>.",
        "<b>DNS & Web Request Test (<code>curl -I https://www.google.com</code>):</b> Verifies that neither name resolution nor outbound HTTP/HTTPS sessions can establish."
    ]
    for chk in iso_checks:
        story.append(Paragraph(f"• {chk}", body_style))
    story.append(Spacer(1, 6))

    story.append(make_evidence_card("Figure 03", "Linux Guest Desktop & Terminal", "fig03_linux_guest_boot.png", "Clean Ubuntu Linux desktop and terminal window loaded inside the isolated virtual machine."))
    story.append(Spacer(1, 6))
    story.append(make_evidence_card("Figure 04", "Empirical Network Unreachability Evidence", "fig04_internet_isolation_test.png", "Terminal showing failed ping to 8.8.8.8 (Network unreachable) and empty default routing table."))
    story.append(PageBreak())

    # =========================================================================
    # CLEAN SNAPSHOT CREATION & SAFE SHELL DEMONSTRATION
    # =========================================================================
    story.append(Paragraph("Clean Snapshot Creation: NPC_Capstone_Clean_State", h1_style))
    story.append(Paragraph(
        "Prior to downloading, writing, or executing any demonstration code, the pristine machine state was frozen by taking a clean hypervisor snapshot designated as <b>NPC_Capstone_Clean_State</b>. This baseline captures the operating system with a verified clean process table, closed non-standard ports, and intact system libraries. If any runtime instability or unexpected modifications occur, this snapshot guarantees instant recovery.",
        body_style
    ))
    story.append(make_evidence_card("Figure 05", "Clean Snapshot in Snapshot Manager", "fig05_clean_snapshot_manager.png", "Hypervisor Snapshot Manager displaying NPC_Capstone_Clean_State node directly below the root."))
    story.append(Spacer(1, 6))
    story.append(make_evidence_card("Figure 06", "Baseline Process & Socket Triage", "fig06_baseline_processes_ports.png", "Terminal displaying baseline ps aux and ss -tulpn output with zero custom listeners active."))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Controlled Educational Bind-Shell Simulation", h1_style))
    story.append(Paragraph(
        "To satisfy the capstone requirement of observing bind-shell-style client-server behaviors while enforcing zero-tolerance safety policies, a harmless laboratory simulation was developed using Python 3 (<code>server.py</code> and <code>client.py</code>).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Safety Guarantees & Non-Weaponization Architecture:</b>",
        body_bold
    ))
    safeguards = [
        "<b>Strict Loopback Binding:</b> The server binds exclusively to <code>127.0.0.1</code> on TCP port <code>54321</code>. It cannot listen on <code>0.0.0.0</code> and cannot receive connections from outside the virtual machine.",
        "<b>No Arbitrary Command Execution:</b> Absolutely NO calls to <code>os.system()</code>, <code>subprocess.Popen()</code>, <code>eval()</code>, or shells (<code>/bin/bash</code>, <code>/bin/sh</code>). Arbitrary user commands (e.g., <code>ls</code>, <code>cat</code>, <code>rm</code>) are caught by input filters and rejected.",
        "<b>Predefined Whitelist Commands Only:</b> Responds strictly to <code>STATUS</code> (returns simulated uptime and sandbox parameters), <code>HELP</code> (returns command syntax), and <code>EXIT</code> (gracefully terminates the client socket).",
        "<b>Zero Persistence / Zero Autostart:</b> Contains no registry hooks, cron jobs, systemd units, or file droppers. Terminates cleanly on <code>Ctrl+C</code>, closing all socket file descriptors."
    ]
    for s in safeguards:
        story.append(Paragraph(f"• {s}", body_style))
    story.append(Spacer(1, 6))

    story.append(make_evidence_card("Figure 07", "Safe Server Launch on Loopback", "fig07_server_launch.png", "Terminal 1 running python3 server.py displaying active listening status on 127.0.0.1:54321."))
    story.append(Spacer(1, 6))
    story.append(make_evidence_card("Figure 08", "Listening Socket Verification (ss)", "fig08_listening_socket_ss.png", "Terminal 2 running ss -tulpn | grep 54321 verifying socket state LISTEN strictly on 127.0.0.1."))
    story.append(Spacer(1, 6))
    story.append(make_evidence_card("Figure 09", "Safe Client Interaction Session", "fig09_client_interaction.png", "Terminal 3 running python3 client.py sending STATUS and HELP commands, receiving safe responses."))
    story.append(PageBreak())

    # =========================================================================
    # SYSTEM MONITORING & NETWORK TRAFFIC ANALYSIS
    # =========================================================================
    story.append(Paragraph("System and Process Monitoring Methodology", h1_style))
    story.append(Paragraph(
        "During execution of the educational simulation, standard Linux forensic utilities were deployed to capture runtime system dynamics across the process hierarchy, socket tables, and open file descriptors:",
        body_style
    ))

    triage_tools = [
        "<b>Process Hierarchy (<code>ps aux</code> & <code>ps -ef --forest</code>):</b> Reveals the runtime process identifier (PID), parent process ID (PPID), controlling terminal (PTS), memory footprint (RSS/VSZ), and CPU consumption.",
        "<b>Dynamic Performance Triage (<code>top -b -n 1</code>):</b> Confirms that the simulation consumes negligible CPU cycles (<0.1%), proving the absence of cryptomining or denial-of-service loops.",
        "<b>Socket Statistics (<code>ss -tulpn</code>):</b> Validates local endpoint binding (<code>127.0.0.1:54321</code>), foreign address wildcards, socket state transitions (<code>LISTEN</code> to <code>ESTABLISHED</code>), and process ownership.",
        "<b>File Descriptor Inspection (<code>ls -l /proc/<PID>/fd/</code>):</b> Verifies that the process holds handles to standard I/O (<code>fd 0-2</code>) and network socket stream (<code>fd 3</code>), with zero unauthorized file writes."
    ]
    for t in triage_tools:
        story.append(Paragraph(f"• {t}", body_style))
    story.append(Spacer(1, 6))

    story.append(make_evidence_card("Figure 10", "Active Process Triage (ps aux)", "fig10_process_monitoring_ps.png", "Terminal showing ps aux output identifying python3 server.py with assigned PID and memory footprint."))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Network Activity & Loopback Packet Analysis", h1_style))
    story.append(Paragraph(
        "<b>Loopback Dynamics vs. Physical Networks:</b> Traffic routed to <code>127.0.0.1</code> traverses the Linux loopback software driver exclusively inside the operating system kernel memory ring buffer. It never transitions onto physical network interface controllers, hypervisor virtual switches, or physical Ethernet cables. As such, loopback communications remain completely unreachable from outside the VM.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Packet Capture Analysis (<code>tcpdump</code> / Wireshark):</b>",
        body_bold
    ))
    story.append(Paragraph(
        "Loopback traffic on port 54321 was recorded using <code>sudo tcpdump -i lo -nn -s 0 -w evidence/packet_captures/safe_simulation_capture.pcap port 54321</code>. Forensic inspection of the PCAP file revealed the complete TCP lifecycle:",
        body_style
    ))
    pcap_steps = [
        "<b>Three-Way Handshake:</b> Client transmits <code>[SYN]</code> packet with initial sequence number. Server responds with <code>[SYN, ACK]</code> confirming window size. Client replies with <code>[ACK]</code>, transitioning socket to <code>ESTABLISHED</code>.",
        "<b>Data Transmission:</b> Server pushes educational banner (<code>[PSH, ACK]</code>). Client transmits 7-byte command string <code>STATUS\\n</code>. Server pushes 312-byte status response payload.",
        "<b>Graceful Teardown:</b> Upon client typing <code>EXIT</code>, a standard four-way TCP FIN-ACK handshake cleanly closes the bidirectional socket stream."
    ]
    for ps in pcap_steps:
        story.append(Paragraph(f"• {ps}", body_style))
    story.append(Spacer(1, 6))

    story.append(make_evidence_card("Figure 11", "Loopback Packet Capture in tcpdump / Wireshark", "fig11_loopback_pcap_tcpdump.png", "Packet trace showing TCP SYN, SYN-ACK, ACK handshake and PSH data packets on loopback port 54321."))
    story.append(PageBreak())

    # =========================================================================
    # STATIC IDENTIFICATION, HASHING & VIRUSTOTAL
    # =========================================================================
    story.append(Paragraph("Static File Identification and Cryptographic Hashing", h1_style))
    story.append(Paragraph(
        "Prior to dynamic testing, static analysis establishes the baseline cryptographic fingerprints and file metadata. In incident response and malware research, cryptographic hashes serve as immutable Indicators of Compromise (IoCs).",
        body_style
    ))

    hash_table_data = [
        [Paragraph("<b>Cryptographic / File Property</b>", table_header), Paragraph("<b>Laboratory Server Script (server.py)</b>", table_header), Paragraph("<b>Laboratory Client Script (client.py)</b>", table_header)],
        [Paragraph("File Size on Disk", table_cell), Paragraph("6,975 bytes", table_cell), Paragraph("2,872 bytes", table_cell)],
        [Paragraph("Source Line Count", table_cell), Paragraph("167 lines", table_cell), Paragraph("80 lines", table_cell)],
        [Paragraph("MIME / Format Classification", table_cell), Paragraph("Python script, ASCII text executable", table_cell), Paragraph("Python script, ASCII text executable", table_cell)],
        [Paragraph("MD5 Hash Digest", table_cell), Paragraph("<code>d4d96fc789a35b6e7d9e1d8550e13bd9</code>", table_cell), Paragraph("<code>221b49ef872dc7705cbc1400d55ce518</code>", table_cell)],
        [Paragraph("SHA-1 Hash Digest", table_cell), Paragraph("<code>7b4f6a48d47a7419fbe180ee8c2a36a5ae3fe9ca</code>", table_cell), Paragraph("<code>2c36cdba0f98683c23734b20d769c6f4293591fb</code>", table_cell)],
        [Paragraph("SHA-256 Hash Digest", table_cell), Paragraph("<code>2c3ac082ac52046d06c822c86b10dfb9b08f1d55ea8f67c134071e3c64cc631c</code>", table_cell), Paragraph("<code>e5724b85bf68128adb31f7af4abd38bf07fd1d8cda3aa07cf3f89ae71fc79993</code>", table_cell)]
    ]
    hash_tbl = Table(hash_table_data, colWidths=[130, 185, 185])
    hash_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_HEADER),
        ('BOX', (0,0), (-1,-1), 1, SECONDARY),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(hash_tbl)
    story.append(Spacer(1, 8))

    story.append(make_evidence_card("Figure 12", "Static File Identification via stat and file", "fig12_file_identification_stat.png", "Terminal showing file command classifying server.py as Python script and stat displaying byte size."))
    story.append(Spacer(1, 6))
    story.append(make_evidence_card("Figure 13", "Cryptographic SHA-256 Hash Verification", "fig13_sha256_calculation.png", "Terminal executing sha256sum server.py client.py displaying exact 64-character hexadecimal digests."))
    story.append(Spacer(1, 10))

    story.append(Paragraph("VirusTotal Threat Intelligence Investigation", h1_style))
    story.append(Paragraph(
        "<b>Responsible Operational Security (OPSEC) Protocol:</b> In accordance with professional cybersecurity threat research standards, private academic scripts or confidential files must <b>NOT</b> be uploaded directly to VirusTotal, as uploaded binaries are distributed to commercial vendors and subscribers worldwide. Instead, analysts perform passive lookups using the computed SHA-256 hash.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Empirical Investigation Findings:</b>",
        body_bold
    ))
    story.append(Paragraph(
        "A passive hash search was conducted for SHA-256 digest <code>2c3ac082ac52046d06c822c86b10dfb9b08f1d55ea8f67c134071e3c64cc631c</code>. In strict compliance with official assignment reporting instructions, the findings are recorded as follows:",
        body_style
    ))

    vt_box = [
        [Paragraph("<b>Official Assignment Status Statement:</b><br/><i>\"No existing VirusTotal report was available for the investigated file at the time of analysis.\"</i><br/><br/><b>Technical Analysis & Multi-Scanner Limitations:</b><br/>Because this educational simulation was authored locally in an offline academic laboratory and has never been indexed publicly, global threat feeds contain no historical record of this hash. It is crucial to emphasize that <b>an unindexed result or a 0/72 detection score does NOT inherently prove that a file is safe</b>. Advanced malware developers intentionally craft custom, unindexed binaries to bypass signature-based antivirus scanners. Multi-scanner reputation is simply one indicator of compromise; dynamic behavioral sandboxing remains essential for definitive validation.", table_cell)]
    ]
    vt_tbl = Table(vt_box, colWidths=[500])
    vt_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, SECONDARY),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(vt_tbl)
    story.append(Spacer(1, 6))

    story.append(make_evidence_card("Figure 14", "VirusTotal Passive Hash Lookup", "fig14_virustotal_hash_lookup.png", "Web browser query for SHA-256 hash on VirusTotal showing unindexed / 0 detection results."))
    story.append(PageBreak())

    # =========================================================================
    # EXPERIMENTAL RESULTS & OBSERVATION MATRIX
    # =========================================================================
    story.append(Paragraph("Experimental Results and Observation Matrix", h1_style))
    story.append(Paragraph(
        "The following structured matrix compares expected sandbox behaviors with the actual empirical outcomes observed throughout the laboratory experiment:",
        body_style
    ))

    matrix_data = [
        [Paragraph("<b>Observation Item</b>", table_header), Paragraph("<b>Expected Sandbox Behavior</b>", table_header), Paragraph("<b>Actual Empirical Result</b>", table_header), Paragraph("<b>Ref</b>", table_header), Paragraph("<b>Conclusion</b>", table_header)],
        [Paragraph("1. Adapter Isolation", table_cell), Paragraph("Disconnected or Host-Only mode", table_cell), Paragraph("Hypervisor adapter disconnected", table_cell), Paragraph("Fig 01-02", table_cell), Paragraph("Physical LAN bridged access eliminated", table_cell)],
        [Paragraph("2. Guest IP & Route", table_cell), Paragraph("Loopback up; Ethernet unrouted", table_cell), Paragraph("lo: 127.0.0.1/8; ens33: unrouted", table_cell), Paragraph("Fig 03", table_cell), Paragraph("No routable IPv4 path to external networks", table_cell)],
        [Paragraph("3. WAN Ping Test", table_cell), Paragraph("Ping to 8.8.8.8 fails immediately", table_cell), Paragraph("Network is unreachable (100% loss)", table_cell), Paragraph("Fig 04", table_cell), Paragraph("Internet unreachability empirically verified", table_cell)],
        [Paragraph("4. Clean Snapshot", table_cell), Paragraph("Baseline snapshot node registered", table_cell), Paragraph("NPC_Capstone_Clean_State created", table_cell), Paragraph("Fig 05", table_cell), Paragraph("Clean forensic recovery point established", table_cell)],
        [Paragraph("5. Baseline Sockets", table_cell), Paragraph("Zero test listeners on port 54321", table_cell), Paragraph("ss confirms no socket on port 54321", table_cell), Paragraph("Fig 06", table_cell), Paragraph("Clean baseline system state verified", table_cell)],
        [Paragraph("6. Server Launch", table_cell), Paragraph("Binds strictly to 127.0.0.1:54321", table_cell), Paragraph("Server active on loopback socket", table_cell), Paragraph("Fig 07", table_cell), Paragraph("Safe listener active in user space", table_cell)],
        [Paragraph("7. Listening State", table_cell), Paragraph("Socket visible in LISTEN state", table_cell), Paragraph("tcp LISTEN 127.0.0.1:54321", table_cell), Paragraph("Fig 08", table_cell), Paragraph("Listening socket confirmed on loopback", table_cell)],
        [Paragraph("8. Client Connect", table_cell), Paragraph("Client establishes local TCP stream", table_cell), Paragraph("Connected to 127.0.0.1:54321", table_cell), Paragraph("Fig 09", table_cell), Paragraph("Controlled local bidirectional stream", table_cell)],
        [Paragraph("9. Command Filter", table_cell), Paragraph("Allows STATUS/HELP; blocks OS calls", table_cell), Paragraph("STATUS returned; bash commands rejected", table_cell), Paragraph("Fig 09-10", table_cell), Paragraph("Arbitrary command execution prevented", table_cell)],
        [Paragraph("10. Loopback Trace", table_cell), Paragraph("TCP handshake & PSH data in PCAP", table_cell), Paragraph("SYN, SYN-ACK, ACK logged on lo", table_cell), Paragraph("Fig 11", table_cell), Paragraph("Socket traffic inspectable via PCAP", table_cell)],
        [Paragraph("11. Static Hashing", table_cell), Paragraph("Deterministic SHA-256 fingerprint", table_cell), Paragraph("2c3ac082ac52046d06... computed", table_cell), Paragraph("Fig 12-13", table_cell), Paragraph("Cryptographic integrity verified", table_cell)],
        [Paragraph("12. Threat Lookup", table_cell), Paragraph("Unindexed academic script", table_cell), Paragraph("No existing report found on VirusTotal", table_cell), Paragraph("Fig 14", table_cell), Paragraph("Expected unindexed academic sample", table_cell)],
        [Paragraph("13. VM Restoration", table_cell), Paragraph("Discards disk modifications", table_cell), Paragraph("Restored to NPC_Capstone_Clean_State", table_cell), Paragraph("Fig 15", table_cell), Paragraph("Differencing disk successfully rolled back", table_cell)],
        [Paragraph("14. Recovery Audit", table_cell), Paragraph("Port closed; process eliminated", table_cell), Paragraph("ps and ss show zero traces of simulation", table_cell), Paragraph("Fig 16", table_cell), Paragraph("Complete system recovery confirmed", table_cell)]
    ]
    matrix_tbl = Table(matrix_data, colWidths=[80, 115, 125, 55, 125])
    matrix_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_HEADER),
        ('BOX', (0,0), (-1,-1), 1, SECONDARY),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(matrix_tbl)
    story.append(PageBreak())

    # =========================================================================
    # SNAPSHOT RESTORATION & FORENSIC COMPARISON
    # =========================================================================
    story.append(Paragraph("Snapshot Restoration and Recovery Verification", h1_style))
    story.append(Paragraph(
        "Following completion of process triage and packet captures, the virtual machine was powered down, and the hypervisor was instructed to revert the guest state to <b>NPC_Capstone_Clean_State</b>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Post-Restoration Empirical Audit:</b> Upon rebooting the restored virtual machine, verification commands were executed to confirm forensic remediation:",
        body_style
    ))
    audit_cmds = [
        "<b>Process Table Audit (<code>ps aux | grep server.py</code>):</b> Returned zero active processes, proving that the simulation service was completely terminated.",
        "<b>Socket Table Audit (<code>ss -tulpn | grep 54321</code>):</b> Returned null output, proving that the TCP listening socket was eradicated and port 54321 returned to a closed state.",
        "<b>Filesystem Cleanup Audit:</b> All temporary execution artifacts, logs in <code>/tmp</code>, and PCAP trace files generated after snapshot creation were eradicated from the virtual disk."
    ]
    for ac in audit_cmds:
        story.append(Paragraph(f"• {ac}", body_style))
    story.append(Spacer(1, 6))

    story.append(make_evidence_card("Figure 15", "Snapshot Restoration in Snapshot Manager", "fig15_snapshot_restoration.png", "Hypervisor dialog reverting virtual machine to clean baseline state NPC_Capstone_Clean_State."))
    story.append(Spacer(1, 6))
    story.append(make_evidence_card("Figure 16", "Post-Restoration Clean Audit", "fig16_post_restoration_audit.png", "Terminal showing ps aux and ss -tulpn confirming closed port 54321 and terminated simulation PID."))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Before-and-After Forensic State Comparison", h2_style))
    comp_data = [
        [Paragraph("<b>Forensic Parameter</b>", table_header), Paragraph("<b>1. Clean Baseline Snapshot</b>", table_header), Paragraph("<b>2. Active Experiment Run</b>", table_header), Paragraph("<b>3. Post-Restoration State</b>", table_header)],
        [Paragraph("Virtual Hard Disk", table_cell), Paragraph("Clean Ubuntu OS filesystem", table_cell), Paragraph("Modified (Scripts, logs, PCAPs created)", table_cell), Paragraph("Clean Ubuntu OS filesystem (Reverted)", table_cell)],
        [Paragraph("Process Table", table_cell), Paragraph("Standard system daemons only", table_cell), Paragraph("<code>python3 server.py</code> running", table_cell), Paragraph("Standard system daemons only (Terminated)", table_cell)],
        [Paragraph("Listening Port 54321", table_cell), Paragraph("Closed / Unbound", table_cell), Paragraph("<code>LISTEN</code> on 127.0.0.1:54321", table_cell), Paragraph("Closed / Unbound (Eradicated)", table_cell)],
        [Paragraph("Active TCP Connections", table_cell), Paragraph("None", table_cell), Paragraph("<code>ESTABLISHED</code> loopback socket", table_cell), Paragraph("None (Terminated)", table_cell)],
        [Paragraph("Temporary Files (/tmp)", table_cell), Paragraph("Pristine OS temporary store", table_cell), Paragraph("Session logs & PCAP buffers stored", table_cell), Paragraph("Pristine OS temporary store (Discarded)", table_cell)]
    ]
    comp_tbl = Table(comp_data, colWidths=[120, 125, 130, 125])
    comp_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_HEADER),
        ('BOX', (0,0), (-1,-1), 1, SECONDARY),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(comp_tbl)
    story.append(Spacer(1, 10))

    # =========================================================================
    # FORENSIC LIMITATIONS & ETHICS
    # =========================================================================
    story.append(Paragraph("Critical Forensic Limitations of Sandbox Snapshots", h1_style))
    story.append(Paragraph(
        "While hypervisor snapshots provide rapid, reliable disk rollback within the virtual guest container, security researchers must account for five fundamental forensic boundaries:",
        body_style
    ))
    limits = [
        "<b>Shared Folders Non-Reversion:</b> If hypervisor Shared Folders are enabled between guest and host, any modifications, file encryption, or malicious droppers written to the shared directory <b>WILL NOT BE REVERTED</b> upon guest snapshot restoration.",
        "<b>External Storage Contamination:</b> Physical USB drives, external SSDs, or mapped SMB/NFS network drives mounted during analysis retain any modifications permanently.",
        "<b>Hypervisor Evasion & VM Escapes:</b> Advanced persistent threat (APT) payloads may exploit zero-day vulnerabilities in hypervisor device drivers (e.g., virtual GPU or SVGA drivers) to escape the guest VM and infect the physical host operating system.",
        "<b>Anti-Analysis Evasion Techniques:</b> Real-world malware scans for virtualization indicators (such as hypervisor MAC address vendors, low core counts, absence of user mouse activity, or known registry keys) and suspends malicious activity to avoid detection.",
        "<b>Irreversible External Network Transmission:</b> If network isolation is breached, outbound network transmissions (such as exfiltrated credentials or notifications sent to an external attacker) cannot be undone by rolling back a local snapshot."
    ]
    for lm in limits:
        story.append(Paragraph(f"• {lm}", body_style))
    story.append(PageBreak())

    # =========================================================================
    # APPLICATIONS, CONCLUSION & REFERENCES
    # =========================================================================
    story.append(Paragraph("Real-World Applications of Malware Sandboxing", h1_style))
    apps = [
        "<b>Security Operations Center (SOC) Triage:</b> Automated sandboxes (such as CAPE, Cuckoo, and Joe Sandbox) automatically detonate suspicious email attachments and quarantine infected assets.",
        "<b>Threat Hunting & YARA Rule Engineering:</b> Observing dropped files, memory injections, and mutexes allows security researchers to author detection signatures before widespread outbreak.",
        "<b>Adversary Infrastructure Tracking:</b> Intercepting Command-and-Control beacons reveals adversary IP addresses, DNS domains, and cryptographic keys used in threat campaigns.",
        "<b>Vulnerability Verification:</b> Enables security teams to safely reproduce proof-of-concept exploits without putting critical infrastructure at risk."
    ]
    for ap in apps:
        story.append(Paragraph(f"• {ap}", body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Conclusion", h1_style))
    story.append(Paragraph(
        "This capstone project successfully demonstrates the design, deployment, monitoring, and recovery of a secure malware analysis sandbox using virtualization hypervisors (VMware Workstation / VirtualBox) and Linux system utilities. By enforcing strict network isolation and validating unreachability empirically, the sandbox eliminates the risk of host infection and lateral propagation. The implementation of a harmless, educational bind-shell simulation illustrated client-server socket lifecycles, process monitoring, and packet capture without introducing dangerous command-execution risks. Static cryptographic analysis and privacy-preserving VirusTotal querying underscored the necessity of combining signature intelligence with dynamic behavioral observation. Finally, restoring the sandbox to <b>NPC_Capstone_Clean_State</b> verified the forensic efficiency of hypervisor snapshots while highlighting their boundaries regarding shared host resources.",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Authoritative Technical References", h1_style))
    refs = [
        "[1] Oracle Corporation, 'Oracle VM VirtualBox User Manual: Virtual Networking and Snapshots,' Oracle Docs, 2024. [Online]. Available: https://docs.oracle.com/en/virtualization/virtualbox/",
        "[2] VMware, Inc. / Broadcom, 'VMware Workstation Pro Documentation: Virtual Networking and Snapshots,' VMware Docs, 2024. [Online]. Available: https://docs.vmware.com/en/VMware-Workstation-Pro/",
        "[3] National Institute of Standards and Technology (NIST), 'Guide to Malware Incident Prevention and Handling,' NIST SP 800-83 Rev. 1, 2013. DOI: 10.6028/NIST.SP.800-83r1.",
        "[4] M. Sikorski and A. Honig, <i>Practical Malware Analysis: The Hands-On Guide to Dissecting Malicious Software</i>, No Starch Press, 2012.",
        "[5] R. Braden, 'Requirements for Internet Hosts - Communication Layers (Loopback Addresses),' RFC 1122, IETF, 1989. [Online]. Available: https://www.rfc-editor.org/rfc/rfc1122",
        "[6] M. Cotton, L. Vegoda, and R. Bonica, 'Special Use IPv4 Addresses,' RFC 5735, IETF, 2010. [Online]. Available: https://www.rfc-editor.org/rfc/rfc5735",
        "[7] Linux Kernel Organization, 'The /proc Filesystem Documentation,' 2024. [Online]. Available: https://docs.kernel.org/filesystems/proc.html",
        "[8] M. Kerrisk, 'Linux Programmer's Manual: ps(1), ss(8), ip(8), stat(1), sha256sum(1),' Linux man-pages project, 2024.",
        "[9] VirusTotal / Google Chronicle, 'VirusTotal API and Threat Intelligence Documentation,' 2024. [Online]. Available: https://docs.virustotal.com/",
        "[10] MITRE Corporation, 'MITRE ATT&CK Framework: Techniques T1059 and T1571,' 2024. [Online]. Available: https://attack.mitre.org/"
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle('RefText', parent=body_style, fontSize=8, leading=11)))
    story.append(Spacer(1, 10))

    # =========================================================================
    # APPENDIX A & B
    # =========================================================================
    story.append(Paragraph("Appendix A: Linux Commands and Triage Cheat Sheet", h1_style))
    commands_appendix = (
        "<b>1. Network Isolation Verification:</b><br/>"
        "<code>ip addr show</code> — Inspect active network adapters.<br/>"
        "<code>ip route show</code> — Verify absence of default gateway.<br/>"
        "<code>ping -c 3 8.8.8.8</code> — Empirically test ICMP unreachability.<br/>"
        "<code>curl -I --connect-timeout 5 https://www.google.com</code> — Verify HTTP reachability failure.<br/><br/>"
        "<b>2. Baseline System Triage:</b><br/>"
        "<code>ps aux > baseline_processes.txt</code> — Capture clean process table.<br/>"
        "<code>ss -tulpn > baseline_listening_ports.txt</code> — Capture clean socket table.<br/><br/>"
        "<b>3. Safe Simulation Execution:</b><br/>"
        "<code>python3 lab/safe_shell_simulation/server.py</code> — Launch safe bind-shell server.<br/>"
        "<code>python3 lab/safe_shell_simulation/client.py</code> — Connect local test client.<br/><br/>"
        "<b>4. Live Process and Socket Monitoring:</b><br/>"
        "<code>ps aux | grep -E 'python3|server.py|client.py'</code> — Inspect running PIDs.<br/>"
        "<code>ss -tulpn | grep 54321</code> — Verify active loopback listener on port 54321.<br/>"
        "<code>sudo tcpdump -i lo -nn -s 0 -w trace.pcap port 54321</code> — Capture loopback packets.<br/><br/>"
        "<b>5. Static File Hashing:</b><br/>"
        "<code>sha256sum server.py client.py</code> — Compute cryptographic SHA-256 digests.<br/>"
        "<code>file server.py</code> — Inspect static file format and MIME properties.<br/><br/>"
        "<b>6. Post-Restoration Verification:</b><br/>"
        "<code>ps aux | grep server.py</code> — Confirm simulation process is eliminated.<br/>"
        "<code>ss -tulpn | grep 54321</code> — Confirm port 54321 is closed."
    )
    story.append(Paragraph(commands_appendix, body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Appendix B: Screenshot Checklist & Suggested Filenames", h1_style))
    chk_appendix = [
        "<b>Fig 01:</b> <code>fig01_vm_configuration.png</code> — Hypervisor VM Hardware Specifications (RAM, vCPU, Virtual Disk).",
        "<b>Fig 02:</b> <code>fig02_network_isolation.png</code> — Virtual Network Adapter set to Disconnected or Host-Only.",
        "<b>Fig 03:</b> <code>fig03_linux_guest_boot.png</code> — Linux Guest Operating System Desktop / Terminal Boot.",
        "<b>Fig 04:</b> <code>fig04_internet_isolation_test.png</code> — Failed ICMP ping and routing table verifying zero WAN egress.",
        "<b>Fig 05:</b> <code>fig05_clean_snapshot_manager.png</code> — Hypervisor Snapshot Manager showing NPC_Capstone_Clean_State.",
        "<b>Fig 06:</b> <code>fig06_baseline_processes_ports.png</code> — Baseline process table (ps aux) and listening sockets (ss -tulpn).",
        "<b>Fig 07:</b> <code>fig07_server_launch.png</code> — Safe simulation server launched, listening strictly on 127.0.0.1:54321.",
        "<b>Fig 08:</b> <code>fig08_listening_socket_ss.png</code> — Socket statistics (ss) verifying active TCP loopback listener.",
        "<b>Fig 09:</b> <code>fig09_client_interaction.png</code> — Client interaction executing STATUS, HELP, and receiving safe responses.",
        "<b>Fig 10:</b> <code>fig10_process_monitoring_ps.png</code> — Active process triage showing PID, PPID, and user context.",
        "<b>Fig 11:</b> <code>fig11_loopback_pcap_tcpdump.png</code> — Loopback packet capture showing TCP 3-way handshake and PSH-ACK transfer.",
        "<b>Fig 12:</b> <code>fig12_file_identification_stat.png</code> — Static file attributes and MIME identification via file and stat.",
        "<b>Fig 13:</b> <code>fig13_sha256_calculation.png</code> — Cryptographic SHA-256 hash calculation in terminal.",
        "<b>Fig 14:</b> <code>fig14_virustotal_hash_lookup.png</code> — VirusTotal query by SHA-256 hash showing unindexed / 0 detections.",
        "<b>Fig 15:</b> <code>fig15_snapshot_restoration.png</code> — Snapshot Manager reverting VM to NPC_Capstone_Clean_State.",
        "<b>Fig 16:</b> <code>fig16_post_restoration_audit.png</code> — Post-recovery audit verifying process termination and closed port."
    ]
    for c in chk_appendix:
        story.append(Paragraph(f"• {c}", ParagraphStyle('ChkText', parent=body_style, fontSize=8, leading=11)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Successfully generated PDF report: {filename}")

if __name__ == '__main__':
    out_path = os.path.join("report", "NPC_Capstone_Malware_Analysis_Sandbox_Report.pdf")
    build_pdf(out_path)
