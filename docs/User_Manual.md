# User Manual — Classical Cryptography Toolkit

**Course:** Network Security  
**Academic Year:** 2026–27 | **Class:** Final Year (ECM)  
**Project Title:** Design and Development of a Classical Cryptography Toolkit  
**Operating System:** Windows 10 / Windows 11  

---

## 1. System Requirements

- **Operating System:** Windows 10 or Windows 11 (64-bit recommended)
- **Python Version:** Python 3.10 to Python 3.14 (Python 3.14 tested)
- **RAM:** Minimum 2 GB (4 GB recommended)
- **Disk Space:** Approximately 250 MB free disk space for dependencies
- **Web Browser:** Any modern browser (Google Chrome, Microsoft Edge, Mozilla Firefox)

---

## 2. Installation & Environment Setup (Windows PowerShell)

Follow these step-by-step commands in **Windows PowerShell** to configure and launch the toolkit.

### Step 1: Open PowerShell and Navigate to the Project Root
```powershell
Set-Location -Path "E:\NS_P"
```

### Step 2: Create a Dedicated Python Virtual Environment
Creating an isolated virtual environment ensures clean dependency management:
```powershell
python -m venv venv
```

### Step 3: Activate the Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```
*(If PowerShell displays an `ExecutionPolicy` restriction, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and then run the activation command above).*

*Git Bash Alternative:*
```bash
source venv/Scripts/activate
```

### Step 4: Upgrade Pip and Install Project Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Verify installed packages:
```powershell
pip list
```

---

## 3. Running Automated Tests

Run the comprehensive pytest test suite to verify algorithm mathematical accuracy:
```powershell
python -m pytest tests -v
```

Expected output:
```text
============================= 51 passed in 0.77s ==============================
```

To run a specific algorithm test (e.g., Caesar Cipher):
```powershell
python -m pytest tests/test_caesar.py -v
```

---

## 4. Starting the Web Application

Launch the Streamlit web dashboard locally:
```powershell
streamlit run app.py
```

Streamlit will start a local server and output:
```text
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

If your web browser does not open automatically, open Google Chrome or Microsoft Edge and navigate to:
**`http://localhost:8501`**

To terminate the application server, press `Ctrl + C` in the PowerShell console.

---

## 5. Navigation & Cipher Instructions

The application features a responsive sidebar with eight core sections:

```
├── 1. Dashboard
├── 2. Substitution Ciphers
├── 3. Transposition Ciphers
├── 4. Compare Algorithms
├── 5. Encrypt Text File
├── 6. Decrypt Text File
├── 7. Help and Documentation
└── 8. About Project
```

### A. Substitution Ciphers View

1. **Caesar Cipher:**
   - **Input Text:** Enter any string (e.g., `NETWORK SECURITY`).
   - **Integer Key:** Enter any integer shift (e.g., `5`). Negative and oversized integers (e.g., `29`, `-21`) are automatically handled modulo 26.
   - **Actions:** Click **🔒 Encrypt** to view ciphertext (`SJYBTWP XJHZWNYD`) or **🔓 Decrypt** to recover plaintext.
   - **Educational Trace:** Inspect the dynamic shift calculation table showing character values and formulas.

2. **Monoalphabetic Substitution Cipher:**
   - **Key Generation:** Click **🎲 Generate Random Key** to automatically produce a verified 26-letter unique substitution alphabet.
   - **Custom Key:** Enter any 26-letter unique alphabet. The system verifies uniqueness and length.
   - **Actions:** Click **🔒 Encrypt** or **🔓 Decrypt**. Letter casing and punctuation are preserved.

3. **Playfair Cipher:**
   - **Keyword:** Enter an alphabetic keyword (e.g., `MONARCHY`).
   - **Matrix View:** Inspect the automatically generated 5×5 key matrix where `I` and `J` are merged.
   - **Preprocessing:** Enter text (e.g., `BALLOON`). Notice how consecutive duplicate letters receive the filler character `'X'` (`BA`, `LX`, `LO`, `ON`).
   - **Actions:** Click **🔒 Encrypt Digraphs** or **🔓 Decrypt Digraphs**.

4. **Hill Cipher (2×2 Matrix mod 26):**
   - **Matrix Selection:** Choose a pre-validated coprime preset (e.g., `[[3, 3], [2, 5]]`) or enter custom integers into the 2×2 matrix grid.
   - **Validation Status:** The system displays the determinant and modular inverse mod 26. Singular or even-determinant matrices are blocked with clear explanations.
   - **Lossless Mode:** Check *"Preserve casing, spaces, and punctuation"* to maintain non-alphabetic formatting.
   - **Actions:** Click **🔒 Encrypt Blocks** or **🔓 Decrypt Blocks**.

5. **Vigenère Cipher:**
   - **Keyword:** Enter an alphabetic keyword (e.g., `LEMON`).
   - **Input Text:** Enter text (e.g., `ATTACKATDAWN`).
   - **Actions:** Click **🔒 Encrypt** (produces `LXFOPVEFRNHR`) or **🔓 Decrypt**. Non-alphabetic symbols do not advance the keyword index.

6. **One-Time Pad (Vernam):**
   - **Key Generation:** Click **🎲 Generate Random Key** to create a cryptographically strong random key matching the message's alphabetic length.
   - **Security Warning:** Read the educational alert detailing Shannon's requirements for true perfect secrecy.
   - **Actions:** Click **🔒 Encrypt (One-Time)** or **🔓 Decrypt with Key**.

---

### B. Transposition Ciphers View

1. **Rail Fence Cipher (Zigzag):**
   - **Rails:** Enter the depth $d \ge 1$ (e.g., `3`).
   - **Actions:** Click **🔒 Encrypt Zigzag** or **🔓 Decrypt Zigzag**.
   - **Visual Grid:** An ASCII zigzag chart demonstrates the exact traversal path.

2. **Columnar Transposition Cipher:**
   - **Keyword:** Enter an alphanumeric key (e.g., `GERMAN`).
   - **Options:** Toggle unpadded irregular transposition (default) or padded mode.
   - **Duplicate Letters:** If key has duplicates (e.g., `BALLOON`), stable left-to-right tie-breaking is applied.
   - **Actions:** Click **🔒 Encrypt Columns** or **🔓 Decrypt Columns**.

---

### C. Algorithm Comparison View

1. Enter a common benchmark payload or use the default network security test string.
2. Select benchmark measurement iterations (1 to 20).
3. Click **🚀 Run Comprehensive Benchmark**.
4. The system measures encryption and decryption times in microseconds using `time.perf_counter()`.
5. View the interactive **Comparative Results Table** and **Matplotlib Execution Time Breakdown Bar Chart**.
6. **Educational Note:** The page explains why algorithmic speed is not an indicator of cryptographic strength.

---

### D. File Encryption and Decryption Views

#### Encrypting a Text File:
1. Navigate to **📁 Encrypt Text File**.
2. Upload any valid UTF-8 `.txt` file via drag-and-drop or file browser.
3. Select desired cipher algorithm and enter key parameters.
4. Click **🔒 Encrypt and Package File**.
5. Click **⬇️ Download Encrypted File (.txt)**.
6. The resulting file includes structured metadata headers:
   ```text
   # ==============================================================
   # CLASSICAL CRYPTOGRAPHY TOOLKIT - ENCRYPTED FILE FORMAT v1.0
   # CIPHER: Caesar Cipher
   # TIMESTAMP: 2026-10-12 13:40:00 UTC
   # METADATA: {"pad_len": 0}
   # ==============================================================
   SJYBTWP XJHZWNYD
   ```

#### Decrypting a Text File:
1. Navigate to **🔓 Decrypt Text File**.
2. Upload the toolkit-encrypted `.txt` file.
3. The toolkit inspects headers and auto-detects the cipher and metadata.
4. Enter the matching decryption key.
5. Click **🔓 Decrypt File** and download the recovered plaintext `.txt` file.

---

## 6. Troubleshooting Common Issues

| Issue / Error | Cause | Recommended Solution |
| :--- | :--- | :--- |
| **`ExecutionPolicy` error in PowerShell** | Restricted Windows PowerShell script execution policy | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in PowerShell before activating `venv`. |
| **`ModuleNotFoundError: No module named 'streamlit'`** | Virtual environment not activated or dependencies missing | Run `.\venv\Scripts\Activate.ps1` followed by `pip install -r requirements.txt`. |
| **Hill Cipher: "Determinant is even"** | Matrix determinant shares factor 2 with 26 | Select coprime preset `[[3, 3], [2, 5]]` or choose numbers where $\det(K) \pmod{26}$ is odd and not 13. |
| **Playfair: "Ciphertext length must be even"** | Playfair decrypts letter pairs (digraphs) | Ensure ciphertext length is an even number of alphabetic characters. |
| **File Decrypt: "Missing toolkit signature"** | Uploaded file was not created by toolkit or headers were altered | Ensure the file begins with `# CLASSICAL CRYPTOGRAPHY TOOLKIT - ENCRYPTED FILE FORMAT v1.0`. |
| **File Decrypt: "Cipher mismatch"** | Attempting to decrypt with a different cipher than encrypted | Use the detected cipher indicated on screen. |

---

## 7. Sample Step-by-Step Workflow

1. Open PowerShell $\rightarrow$ `Set-Location E:\NS_P` $\rightarrow$ `streamlit run app.py`.
2. Browser opens `http://localhost:8501`.
3. Open **Substitution Ciphers** $\rightarrow$ select **Caesar Cipher**.
4. Plaintext: `NETWORK SECURITY`, Key: `5` $\rightarrow$ Click **Encrypt**.
5. Observe output: `SJYBTWP XJHZWNYD`.
6. Open **Encrypt Text File** $\rightarrow$ upload `sample.txt` $\rightarrow$ choose **Hill Cipher** $\rightarrow$ Encrypt and download `encrypted_sample.txt`.
7. Open **Decrypt Text File** $\rightarrow$ upload `encrypted_sample.txt` $\rightarrow$ Click Decrypt $\rightarrow$ Verify recovered text matches `sample.txt`.
8. Open **Compare Algorithms** $\rightarrow$ Click **Run Comprehensive Benchmark** $\rightarrow$ Observe performance metrics and comparative charts.
