# CLASSICAL CRYPTOGRAPHY TOOLKIT
### An Interactive Educational Platform for Classical Encryption, Decryption, and Performance Analysis

![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-red)
![Pytest](https://img.shields.io/badge/Pytest-51%20Passed-brightgreen)
![License](https://img.shields.io/badge/License-Educational-green)

---

## 🛡️ Project Overview

The **Classical Cryptography Toolkit** is an interactive, menu-driven cybersecurity platform designed for final-year engineering students and cybersecurity educators. Built using **Python 3** and **Streamlit**, the application implements eight classical cryptographic algorithms spanning both substitution and transposition cipher families.

The platform provides mathematically verified encryption and decryption, real-time step-by-step traces, key validation with coprime matrix checks, microsecond-precision performance benchmarking (`time.perf_counter()`), and lossless UTF-8 text file processing with structured metadata preservation.

---

## 🎓 Academic Information

- **Course:** Network Security
- **Class:** Final Year, Department of Electronics & Computer Engineering (ECM), 2026–27
- **Student Name:** [ENTER YOUR NAME]
- **Roll Number:** [ENTER YOUR ROLL NUMBER]
- **Batch:** [ENTER YOUR BATCH]
- **Submission Date:** [ENTER SUBMISSION DATE]

---

## ✨ Features

- **8 Classical Cryptographic Algorithms:**
  - **Substitution:** Caesar Cipher, Monoalphabetic Substitution, Playfair Cipher (5×5 Matrix), Hill Cipher (2×2 Matrix mod 26), Vigenère Cipher, One-Time Pad (Vernam).
  - **Transposition:** Rail Fence Cipher (Zigzag), Columnar Transposition Cipher (with stable tie-breaking and irregular row handling).
- **Interactive Cyber-Themed Dashboard:**
  - Modern dark charcoal/navy theme with cyan and emerald accents.
  - Transparent step-by-step mathematical traces, visual matrix layouts, and ASCII zigzag grids.
- **Algorithm Performance Comparison:**
  - Empirical microsecond benchmarks comparing encryption/decryption execution times, memory expansion ratios, and round-trip equality.
  - Interactive visualization via Matplotlib bar charts.
- **Lossless Text File Encryption & Decryption:**
  - Upload and encrypt any standard UTF-8 `.txt` file.
  - Downloads include documented headers (`# CIPHER`, `# TIMESTAMP`, `# METADATA`) enabling automated detection and decryption.
- **Comprehensive Input Validation:**
  - Validates key constraints, coprimality with 26 for Hill matrices, 26-letter unique alphabets, and boundary rail values.
- **Automated Testing Suite:**
  - 51 unit tests executed via `pytest`, achieving a 100% pass rate.

---

## 🧰 Technology Stack

- **Core Backend:** Python 3 (Pure Python mathematical algorithms)
- **Frontend Framework:** Streamlit (Responsive web interface)
- **Testing Framework:** Pytest (51 automated test cases)
- **Data & Plotting:** Pandas & Matplotlib
- **Document Generation:** Python-pptx (PowerPoint presentation generator)

---

## 📂 Project Architecture

```
classical-cryptography-toolkit/
├── app.py                      # Main Streamlit Cyber Dashboard
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git exclusions
├── generate_pptx.py            # Script generating docs/Presentation.pptx
│
├── crypto/                     # Cryptographic Algorithm Engine
│   ├── __init__.py             # Package exports
│   ├── utils.py                # Extended GCD, mod_inverse, coprime helpers
│   ├── caesar.py               # Caesar cipher & step generator
│   ├── monoalphabetic.py       # Monoalphabetic substitution & random key generator
│   ├── playfair.py             # Playfair 5x5 key matrix & digraph handler
│   ├── hill.py                 # Hill cipher (2x2 matrix mod 26) & coprime validation
│   ├── vigenere.py             # Polyalphabetic Vigenère cipher & keyword trace
│   ├── one_time_pad.py         # Vernam One-Time Pad & cryptographic PRNG
│   ├── rail_fence.py           # Rail Fence cipher & ASCII zigzag grid visualizer
│   └── columnar_transposition.py # Columnar transposition (irregular & padded)
│
├── modules/                    # Application Support Modules
│   ├── __init__.py             # Module exports
│   ├── validation.py           # Centralized input/key validator
│   ├── file_handler.py         # UTF-8 text file packaging with headers
│   └── comparison.py           # Multi-iteration performance benchmarking
│
├── tests/                      # Automated Pytest Suite (51 Tests)
│   ├── test_caesar.py
│   ├── test_monoalphabetic.py
│   ├── test_playfair.py
│   ├── test_hill.py
│   ├── test_vigenere.py
│   ├── test_one_time_pad.py
│   ├── test_rail_fence.py
│   ├── test_columnar_transposition.py
│   └── test_file_handler.py
│
├── docs/                       # Academic Deliverables
│   ├── Mini_Project_Report.md  # Formal Academic Project Report
│   ├── User_Manual.md          # Comprehensive User Guide
│   ├── Presentation_Content.md # 6-Slide Presentation Content & Speaker Notes
│   ├── Presentation.pptx       # Generated PowerPoint Presentation
│   └── Test_Cases.md           # Automated test cases & verification log
│
└── screenshots/                # Application Screenshots
    └── README.md               # Capture guide & 5-minute video demo script
```

---

## 🚀 Installation & Launch Guide

### 1. Clone or Open the Repository
```powershell
Set-Location -Path "E:\NS_P"
```

### 2. Set Up a Virtual Environment (Recommended)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Run the Automated Test Suite
```powershell
python -m pytest tests -v
```
*Expected: 51 passed in < 1 second.*

### 5. Launch the Streamlit Application
```powershell
streamlit run app.py
```
Open your browser and navigate to: **`http://localhost:8501`**

---

## 🔍 Sample Caesar Cipher Reference

- **Plaintext:** `NETWORK SECURITY`
- **Key:** `5`
- **Encryption Transformation:**  
  $$C_i = (P_i + 5) \pmod{26}$$
- **Ciphertext Output:** `SJYBTWP XJHZWNYD`
- **Decrypted Output:** `NETWORK SECURITY`

---

## ⚠️ Limitations & Educational Disclaimer

> **IMPORTANT:** Classical cryptographic algorithms are strictly educational and historical. They lack semantic security, integrity protection, and resistance to modern computer-assisted cryptanalysis. Monoalphabetic and polyalphabetic ciphers yield to frequency analysis, small key spaces can be brute-forced instantaneously, and transposition ciphers do not alter symbol frequencies. **Never deploy classical ciphers for confidential, financial, or production communications.** Modern applications mandate authenticated encryption standards such as AES-256-GCM, RSA-4096, and Elliptic Curve Cryptography (ECC).

---

## 📚 References & Credits

1. **Python Documentation:** [https://docs.python.org/3/](https://docs.python.org/3/)
2. **Streamlit Documentation:** [https://docs.streamlit.io/](https://docs.streamlit.io/)
3. **Pytest Testing Framework:** [https://docs.pytest.org/](https://docs.pytest.org/)
4. **Stallings, William.** *Cryptography and Network Security: Principles and Practice*, 8th Edition, Pearson, 2020.
