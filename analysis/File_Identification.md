# File Identification and Static Characteristics

**Student Name:** Chetan Pawar  
**PRN:** 2125UCSM1037  
**Course:** B.Tech Computer Science Engineering (Cyber Security)  
**Institution:** Sanjivani University, Kopargaon  
**Subject:** NPC Capstone Project  
**Academic Year:** 2026–2027  

---

## 1. Objective of File Identification

Before dynamic execution in a malware sandbox, an investigator must perform static file identification to ascertain the file format, architecture target, encoding, header magic bytes, and potential execution requirements without executing code.

---

## 2. Investigated File Profile: `server.py`

| Property | Value / Analysis Result | Verification Method |
| :--- | :--- | :--- |
| **File Name** | `server.py` | Directory listing (`ls -l`) |
| **Relative Path** | `lab/safe_shell_simulation/server.py` | Filesystem path |
| **File Classification** | Educational Bind-Shell Simulation Script | Code audit / Author specification |
| **Malicious Nature** | **BENIGN / HARMLESS SIMULATION** | Confirmed by code inspection |
| **File Format** | Python 3 source script, UTF-8 text executable | `file` utility / MIME detection |
| **File Size (Bytes)** | `6,975 bytes` | `stat -c %s server.py` |
| **Line Count** | 167 lines | `wc -l server.py` |
| **Interpreter Shebang** | `#!/usr/bin/env python3` | Header inspection (Line 1) |
| **Bound Network Port** | TCP `54321` on `127.0.0.1` (Loopback only) | Socket configuration audit |
| **System Calls** | Pure Python socket library; NO `os.system` / `subprocess` | Static AST / Regex inspection |

---

## 3. Investigated File Profile: `client.py`

| Property | Value / Analysis Result | Verification Method |
| :--- | :--- | :--- |
| **File Name** | `client.py` | Directory listing (`ls -l`) |
| **Relative Path** | `lab/safe_shell_simulation/client.py` | Filesystem path |
| **File Classification** | Educational Test Client Utility | Code audit / Author specification |
| **Malicious Nature** | **BENIGN / HARMLESS UTILITY** | Confirmed by code inspection |
| **File Format** | Python 3 source script, UTF-8 text executable | `file` utility / MIME detection |
| **File Size (Bytes)** | `2,872 bytes` | `stat -c %s client.py` |
| **Line Count** | 80 lines | `wc -l client.py` |
| **Interpreter Shebang** | `#!/usr/bin/env python3` | Header inspection (Line 1) |
| **Target Address** | `127.0.0.1:54321` (Local loopback only) | Socket configuration audit |

---

## 4. File Magic and Header Analysis
In Linux, the `file` utility interrogates the initial bytes (magic numbers) of a file rather than trusting file extensions:
```bash
file lab/safe_shell_simulation/server.py
```
*Empirical Output:*
```
server.py: Python script, ASCII text executable, with CRLF line terminators
```

This confirms the artifact is an interpreted script rather than a compiled ELF binary, meaning execution is handled via the system Python 3 runtime interpreter.
