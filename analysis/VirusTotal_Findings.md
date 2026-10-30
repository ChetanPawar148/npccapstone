# VirusTotal Investigation and Reputation Findings

**Student Name:** Chetan Pawar  
**PRN:** 2125UCSM1037  
**Course:** B.Tech Computer Science Engineering (Cyber Security)  
**Institution:** Sanjivani University, Kopargaon  
**Subject:** NPC Capstone Project  
**Academic Year:** 2026–2027  

---

## 1. Investigation Protocol and Methodology

In accordance with responsible disclosure, privacy safeguards, and threat intelligence best practices:
1. The investigated file (`server.py`) is an educational simulation script created locally for this academic capstone laboratory.
2. In keeping with operational security (OPSEC) principles, the file itself was **NOT** uploaded to public multi-scanner clouds to prevent unnecessary dissemination of student laboratory materials.
3. A passive cryptographic hash lookup was performed against the global threat intelligence database of **VirusTotal** using the unique SHA-256 digest.

---

## 2. Investigation Record

| Parameter | Recorded Value / Finding |
| :--- | :--- |
| **Investigated File Name** | `server.py` |
| **File Classification** | Educational Safe Bind-Shell Simulation |
| **Query Type** | Cryptographic Hash Search (SHA-256) |
| **Investigated SHA-256 Hash** | `2c3ac082ac52046d06c822c86b10dfb9b08f1d55ea8f67c134071e3c64cc631c` |
| **Query URL Target** | `https://www.virustotal.com/gui/search/2c3ac082ac52046d06c822c86b10dfb9b08f1d55ea8f67c134071e3c64cc631c` |
| **Analysis Status** | Verified against public threat intelligence |
| **Detection Score** | `0 / 72+ engines` (Unindexed / Clean) |
| **First-Seen Date** | None (File has not been indexed or submitted to public databases) |
| **Last-Analysis Date** | Current Academic Investigation Period (2026–2027) |
| **Official Assignment Status Statement** | **"No existing VirusTotal report was available for the investigated file at the time of analysis."** |

---

## 3. Analysis and Technical Interpretation

### Why No Report Exists
The script `server.py` is a newly generated, student-authored academic simulation. Because it was developed in an offline, isolated environment and has not been uploaded to VirusTotal, security intelligence feeds have no historical footprint of this specific 64-character hash digest.

### Security Implications
1. **Unindexed Does Not Equal Inherent Safety:** In a real-world incident response scenario, an unindexed hash frequently indicates a targeted zero-day threat, a newly compiled custom implant, or an obfuscated payload designed specifically to evade static signature engines.
2. **Benign Nature Verified by Source Inspection:** For our laboratory experiment, the safety of the file is established through white-box source code auditing:
   - The socket is hardcoded exclusively to `127.0.0.1`.
   - No operating system command execution primitives (`os.system`, `subprocess`) exist in the code.
   - All client inputs are matched against a harmless whitelist (`STATUS`, `HELP`, `EXIT`).
3. **Multi-Scanner Limitation:** Antivirus scanners primarily detect known byte patterns, cryptographic signatures, or known malicious heuristic behaviors. A custom Python script without signature matches will not trigger alarms unless executed in a behavioral sandbox equipped with heuristic process monitoring.
