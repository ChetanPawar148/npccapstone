# Cryptographic Hash Results and Integrity Analysis

**Student Name:** Chetan Pawar  
**PRN:** 2125UCSM1037  
**Course:** B.Tech Computer Science Engineering (Cyber Security)  
**Institution:** Sanjivani University, Kopargaon  
**Subject:** NPC Capstone Project  
**Academic Year:** 2026–2027  

---

## 1. The Role of Cryptographic Hashing in Malware Analysis

Cryptographic hash functions map arbitrary-length binary inputs into fixed-length digest strings. In malware analysis and incident response, cryptographic hashing provides five core capabilities:

1. **Deterministic Unique Fingerprinting:** A file produces an identical hash digest whenever processed by the same algorithm.
2. **Avalanche Effect:** Altering even a single bit or whitespace character in the script completely alters the resulting digest, exposing any tampering.
3. **Collision Resistance:** Computationally infeasible for two distinct files to generate the identical SHA-256 hash digest.
4. **Indicator of Compromise (IoC) Sharing:** Threat intelligence platforms (VirusTotal, AlienVault OTX, MISP) catalog malware by SHA-256 rather than file names, which are trivial for attackers to rename.
5. **Chain of Custody & Forensic Verification:** Proves that an evidence sample remained unmodified from the moment of initial triage to final reporting.

---

## 2. Calculated Cryptographic Hashes

The following hashes were computed directly from the laboratory scripts using SHA-256, SHA-1, and MD5 algorithms:

### Laboratory Server Script (`server.py`)
- **File Path:** `lab/safe_shell_simulation/server.py`
- **File Size:** `6,975 bytes`
- **MD5:** `d4d96fc789a35b6e7d9e1d8550e13bd9`
- **SHA-1:** `7b4f6a48d47a7419fbe180ee8c2a36a5ae3fe9ca`
- **SHA-256:**
  ```
  2c3ac082ac52046d06c822c86b10dfb9b08f1d55ea8f67c134071e3c64cc631c
  ```

### Laboratory Client Script (`client.py`)
- **File Path:** `lab/safe_shell_simulation/client.py`
- **File Size:** `2,872 bytes`
- **MD5:** `221b49ef872dc7705cbc1400d55ce518`
- **SHA-1:** `2c36cdba0f98683c23734b20d769c6f4293591fb`
- **SHA-256:**
  ```
  e5724b85bf68128adb31f7af4abd38bf07fd1d8cda3aa07cf3f89ae71fc79993
  ```

---

## 3. How to Calculate and Verify in Linux

Inside the Linux virtual machine terminal, compute and verify the hashes using standard core utilities:

```bash
# Calculate SHA-256 hash
sha256sum lab/safe_shell_simulation/server.py

# Calculate SHA-1 hash
sha1sum lab/safe_shell_simulation/server.py

# Calculate MD5 hash
md5sum lab/safe_shell_simulation/server.py
```

### Integrity Verification File
You can export the hashes to an integrity manifest:
```bash
sha256sum lab/safe_shell_simulation/*.py > checksums.sha256
sha256sum -c checksums.sha256
```
*Expected Output:*
```
lab/safe_shell_simulation/server.py: OK
lab/safe_shell_simulation/client.py: OK
```
