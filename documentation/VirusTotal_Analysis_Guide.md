# VirusTotal Analysis and Threat Intelligence Guide

**Student Name:** Chetan Pawar  
**PRN:** 2125UCSM1037  
**Course:** B.Tech Computer Science Engineering (Cyber Security)  
**Institution:** Sanjivani University, Kopargaon  
**Subject:** NPC Capstone Project  
**Academic Year:** 2026–2027  

---

## 1. What is VirusTotal?

VirusTotal is an online threat intelligence service owned by Google Chronicle. It aggregates over 70 commercial antivirus engines, next-generation endpoint detection and response (EDR) scanners, and heuristic rule engines (e.g., YARA rules, behavioral sandboxes) to evaluate files, domains, IP addresses, and URLs.

---

## 2. Responsible Methodology: Privacy, OPSEC, and Safe Lookup

When dealing with suspicious binaries, scripts, or laboratory samples, cybersecurity researchers adhere to strict Operational Security (OPSEC) and data privacy rules:

### Rule 1: Hash-Based Lookup First (Do NOT Blindly Upload)
- **Why:** Uploading a file to VirusTotal distributes the binary to all participating security vendors and subscribers worldwide.
- **Risks of Uploading:**
  - If the file contains proprietary corporate code, internal credentials, API keys, or personal data, it becomes accessible to third-party researchers.
  - If the file is part of a targeted red team engagement or active cyber incident, uploading alerts threat actors that their custom implant has been discovered.
- **Best Practice:** Always calculate the cryptographic hash (SHA-256) locally and query VirusTotal using the hash search bar (`https://www.virustotal.com/gui/search/<SHA256>`).

### Rule 2: Handling Harmless Educational Scripts
For student-authored simulation scripts like our `server.py`:
- Because the script is newly created and strictly educational, VirusTotal typically returns:
  > *"No matches found"* or *"No existing VirusTotal report was available for the investigated file at the time of analysis."*
- If someone previously submitted a copy, it should report `0 / 70+ engines detected this file` as clean.

### Rule 3: The Danger of "Clean" Reports (False Negatives)
A score of `0/70` **DOES NOT PROVE** a program is safe:
- Zero-day exploits, novel obfuscation, polymorphic packers, and living-off-the-land binaries (LOLBins) easily evade signature engines.
- Heuristic engines may not flag simple scripts unless they contain known malicious strings or signatures.
- Static multi-scanner analysis must always be combined with dynamic behavioral sandboxing.

---

## 3. Step-by-Step VirusTotal Lookup Workflow

```
+-------------------------------------------------------------------------------+
|                      RESPONSIBLE VIRUSTOTAL QUERY WORKFLOW                    |
+-------------------------------------------------------------------------------+
                                        |
                    [ Calculate SHA-256 Hash Locally ]
                   (sha256sum server.py in Linux terminal)
                                        |
                                        v
                 [ Open Web Browser on Host / Analysis PC ]
                   Navigate to: https://www.virustotal.com/
                                        |
                                        v
                    [ Click 'SEARCH' Tab (Search by Hash) ]
                     Paste the 64-character SHA-256 hash
                                        |
                                        v
                       +----------------+----------------+
                       |                                 |
              [ Report Found ]                  [ No Report Found ]
                       |                                 |
       Record:                           Record:
       - Detection Ratio (e.g., 0/72)    "No existing VirusTotal report
       - First-Seen Date                 was available for the investigated
       - Last-Analysis Date              file at the time of analysis."
       - Identified Community Tags                       |
                       +----------------+----------------+
                                        |
                       [ Integrate into Analysis Report ]
+-------------------------------------------------------------------------------+
```

---

## 4. How to Interpret VirusTotal Findings

When a report is located on VirusTotal, review the following primary tabs:

1. **Detection Tab:**
   - **Detection Ratio:** Shows the count of security vendors flagging the sample versus total engines queried (e.g., `52/71` for a known Trojan, or `0/72` for a benign script).
   - **Malware Classification Names:** E.g., `Backdoor.Linux.Shell.A`, `Trojan.GenericKD`, or `HEUR/QVM20.1.0000.Malware`.
2. **Details Tab:**
   - **File Hashes:** MD5, SHA-1, SHA-256, SSDEEP, TLSH.
   - **File Properties:** Exact size, MIME type (`text/x-python`), magic byte identification.
   - **History:** First submission timestamp and most recent scan timestamp.
3. **Behavior Tab (Dynamic Sandbox Results):**
   - Outbound DNS lookups and IP connections observed during cloud execution.
   - Registry changes, dropped files, and invoked system commands.
4. **Community Tab:**
   - Notes, YARA rules, and comments left by global threat researchers.
