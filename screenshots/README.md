# Application Screenshots and Video Demonstration Guide

This directory is designated for storing high-resolution screenshots of the running **Classical Cryptography Toolkit** web application.

---

## 📸 1. Manual Screenshot Capture Instructions (Windows 10/11)

To capture authentic screenshots of your running application:

### Step 1: Launch the Application
In **Windows PowerShell**, ensure your virtual environment is active and execute:
```powershell
Set-Location -Path "E:\NS_P"
streamlit run app.py
```
Open your web browser at **`http://localhost:8501`**.

### Step 2: Capture Screenshots Using Windows Hotkeys
Press **`Windows Key + Shift + S`** (or open **Snipping Tool**), select **Window Snip** or **Rectangular Snip**, and capture each view. Save the files into this `screenshots/` directory using the filenames specified below:

| Target Filename | Application Navigation View | Configuration / Action to Showcase |
| :--- | :--- | :--- |
| **`01_dashboard.png`** | **Dashboard** | Metrics row (8 Ciphers, 51/51 Pytest), educational disclaimer banner, and category overview cards. |
| **`02_caesar_cipher.png`** | **Substitution Ciphers** $\to$ Caesar | Text: `NETWORK SECURITY`, Key: `5`, Click **Encrypt** $\to$ Show ciphertext `SJYBTWP XJHZWNYD` and the Step-by-Step Shift Trace table. |
| **`03_playfair_cipher.png`**| **Substitution Ciphers** $\to$ Playfair | Keyword: `MONARCHY`, Text: `BALLOON`, Click **Encrypt Digraphs** $\to$ Show 5×5 key matrix and digraph rule transformations. |
| **`04_hill_cipher.png`** | **Substitution Ciphers** $\to$ Hill | Preset: `[[3, 3], [2, 5]]`, Text: `HELP`, Click **Encrypt Blocks** $\to$ Show determinant $= 9$, modular inverse matrix, and vector steps. |
| **`05_algorithm_comparison.png`** | **Compare Algorithms** | Benchmark test message, Click **Run Comprehensive Benchmark** $\to$ Show comparative metrics table and Matplotlib bar chart. |
| **`06_file_encryption.png`** | **Encrypt Text File** | Upload a `.txt` file, choose Caesar/Hill cipher, Click **Encrypt and Package File** $\to$ Show download button and header preview. |
| **`07_help_documentation.png`**| **Help and Documentation** | Open tabs: **Cipher Theory**, **Common Errors & Fixes**, and **Classical vs Modern Cryptography**. |

---

## 🎬 2. Five-Minute Video Demonstration Script

**Title:** Classical Cryptography Toolkit — Network Security Mini Project Demo  
**Target Duration:** 4 minutes 45 seconds (Under 5 minutes)  
**Presenter:** [ENTER YOUR NAME], Final Year (ECM), 2026–27  

---

### [00:00 – 00:45] Minute 1: Introduction & Architecture
- **Screen View:** Start on **Dashboard** (`http://localhost:8501`).
- **Visual Action:** Scroll smoothly through the title banner, academic credentials in the sidebar, and key metrics cards.
- **Presenter Narration:**
  > "Hello everyone. My name is [YOUR NAME], and today I am demonstrating my Network Security final-year mini project: the *Classical Cryptography Toolkit*.
  > This toolkit is an interactive educational workbench implementing eight classical algorithms spanning substitution and transposition ciphers.
  > Notice our cybersecurity-themed dark dashboard built with Streamlit. At the top, we highlight an essential educational notice: classical ciphers are historical and insecure for modern confidential data.
  > On the dashboard, we observe that all eight algorithms are fully operational and verified through 51 automated unit tests."

---

### [00:45 – 01:45] Minute 2: Substitution Ciphers (Caesar & Hill)
- **Screen View:** Navigate to **Substitution Ciphers** from the sidebar.
- **Visual Action 1 (Caesar):**
  - Select **Caesar Cipher**.
  - Enter `NETWORK SECURITY` with key `5`.
  - Click **Encrypt**. Highlight `SJYBTWP XJHZWNYD` and expand the shift calculation table.
- **Visual Action 2 (Hill):**
  - Select **Hill Cipher**.
  - Select preset `[[3, 3], [2, 5]]`. Note determinant is 9 mod 26 and inverse exists.
  - Enter `HELP` and click **Encrypt Blocks**. Highlight output `HIAT`.
  - Enter invalid matrix (e.g., `[[2, 4], [1, 2]]` det=0) to demonstrate error rejection.
- **Presenter Narration:**
  > "Let's examine Substitution Ciphers. First, the Caesar Cipher. When we enter the prompt's reference test case 'NETWORK SECURITY' with key 5, we instantly obtain the ciphertext 'SJYBTWP XJHZWNYD'. The toolkit generates an interactive trace demonstrating the exact formula for each letter.
  > Next, let's observe the Hill Cipher operating on a 2 by 2 matrix mod 26. Our validation layer ensures the determinant is coprime with 26. With key matrix 3, 3, 2, 5, the determinant is 9, and the modular inverse matrix is automatically computed. Encrypting 'HELP' yields 'HIAT', matching standard textbook vectors. If an invalid or singular matrix is supplied, the system immediately rejects it with actionable mathematical feedback."

---

### [01:45 – 02:30] Minute 3: Playfair & Transposition Ciphers
- **Screen View:** Switch to **Playfair Cipher**, then navigate to **Transposition Ciphers**.
- **Visual Action 1 (Playfair):**
  - Keyword: `MONARCHY`, Text: `BALLOON`. Click **Encrypt Digraphs**. Point to 5×5 matrix with merged I/J and filler 'X' in `LX`.
- **Visual Action 2 (Rail Fence):**
  - Switch to **Transposition Ciphers** $\to$ **Rail Fence**.
  - Rails: `3`, Text: `DEFEND THE EAST WALL`. Click **Encrypt Zigzag**. Show ASCII zigzag grid.
- **Presenter Narration:**
  > "In the Playfair Cipher, entering keyword 'MONARCHY' automatically builds a 5 by 5 key matrix merging I and J. Notice that entering 'BALLOON' correctly triggers our preprocessing rule, inserting filler letter 'X' between the duplicate L's.
  > Moving to Transposition Ciphers, our Rail Fence cipher writes characters in a diagonal zigzag pattern across a configurable number of rails. The ASCII grid visualizer illustrates the geometric path, preserving spaces and casing."

---

### [02:30 – 03:30] Minute 4: Microsecond Performance Benchmarking
- **Screen View:** Navigate to **Compare Algorithms**.
- **Visual Action:**
  - Keep default payload or type custom text. Set iterations to 5.
  - Click **🚀 Run Comprehensive Benchmark**.
  - Review the results table and Matplotlib bar chart.
- **Presenter Narration:**
  > "Now, let's explore our performance comparison module. Here, we benchmark all eight algorithms on a common payload using Python's high-resolution `time.perf_counter()`.
  > Clicking 'Run Benchmark' measures encryption and decryption latencies in microseconds. We see that stream ciphers like Caesar and Vigenère execute in under 20 microseconds, while matrix and grid-based ciphers like Hill and Playfair require approximately 40 to 50 microseconds.
  > Most importantly, we provide an educational disclaimer: raw speed does not correlate with security. Caesar is the fastest algorithm here, yet it possesses only 25 keys and is trivially broken in milliseconds."

---

### [03:30 – 04:15] Minute 5: Text File Operations & Testing
- **Screen View:** Navigate to **Encrypt Text File**, then **Decrypt Text File**.
- **Visual Action 1:**
  - Upload `sample.txt`, choose Caesar key `7`, click **Encrypt and Package File**, and download.
  - Open downloaded file in Notepad to reveal `# CIPHER` and `# METADATA` headers.
- **Visual Action 2:**
  - Upload the encrypted file into **Decrypt Text File**. Note auto-detection of cipher. Decrypt and verify matching plaintext.
- **Presenter Narration:**
  > "Our file module allows users to encrypt and decrypt arbitrary UTF-8 text files. When we encrypt a document, the toolkit packages it with a documented header containing the cipher type, timestamp, and padding metadata.
  > Uploading this file to the Decrypt module automatically reads the header, prompts for the key, and restores the exact original document without formatting corruption."

---

### [04:15 – 04:45] Conclusion & Evaluation Wrap-up
- **Screen View:** Return to **Dashboard** or **About Project**.
- **Presenter Narration:**
  > "To verify complete software reliability, we executed 51 automated unit tests with pytest, achieving a 100% pass rate.
  > In conclusion, the Classical Cryptography Toolkit fulfills all academic objectives for our Network Security mini project, bridging historical cipher theory and modern interactive software design. Thank you for your time."
