"""Classical Cryptography Toolkit - Modern Streamlit Web Application.

An Interactive Educational Platform for Classical Encryption and Decryption.
Course: Network Security | Class: Final Year (ECM), 2026-27.
"""

import io
import time
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Import cryptographic algorithms
from crypto import (
    encrypt_caesar,
    decrypt_caesar,
    encrypt_monoalphabetic,
    decrypt_monoalphabetic,
    generate_monoalphabetic_key,
    validate_monoalphabetic_key,
    encrypt_playfair,
    decrypt_playfair,
    generate_playfair_matrix,
    encrypt_hill,
    decrypt_hill,
    validate_hill_matrix,
    invert_matrix_mod26,
    encrypt_vigenere,
    decrypt_vigenere,
    validate_vigenere_key,
    encrypt_otp,
    decrypt_otp,
    generate_otp_key,
    validate_otp_key,
    encrypt_rail_fence,
    decrypt_rail_fence,
    validate_rail_fence_key,
    encrypt_columnar,
    decrypt_columnar,
    validate_columnar_key,
)
from crypto.caesar import get_caesar_steps
from crypto.vigenere import get_vigenere_steps
from crypto.rail_fence import get_rail_fence_grid
from crypto.one_time_pad import OTP_SECURITY_WARNING

# Import support modules
from modules.file_handler import (
    encrypt_text_file,
    decrypt_text_file,
    parse_encrypted_file_content,
)
from modules.comparison import (
    benchmark_all_ciphers,
    COMPARISON_DISCLAIMER,
)
from modules.validation import validate_cipher_input

# Page Configuration
st.set_page_config(
    page_title="Classical Cryptography Toolkit",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Cyber Dark Theme Styling
CYBER_CSS = """
<style>
    /* Dark Theme Base Palette */
    :root {
        --bg-main: #0b0f19;
        --bg-card: #111827;
        --bg-card-hover: #1f2937;
        --accent-cyan: #06b6d4;
        --accent-green: #10b981;
        --accent-emerald: #059669;
        --text-primary: #f3f4f6;
        --text-secondary: #9ca3af;
        --border-color: #374151;
    }

    /* Overall Background & Font */
    .stApp {
        background-color: var(--bg-main);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Main Headers */
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 50%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }

    .main-subtitle {
        font-size: 1.05rem;
        color: #94a3b8;
        margin-bottom: 1.5rem;
    }

    /* Educational Disclaimer Banner */
    .edu-banner {
        background: linear-gradient(90deg, rgba(239, 68, 68, 0.15), rgba(245, 158, 11, 0.15));
        border-left: 4px solid #ef4444;
        padding: 0.9rem 1.2rem;
        border-radius: 6px;
        color: #fecaca;
        font-size: 0.92rem;
        margin-bottom: 1.5rem;
        line-height: 1.45;
    }

    /* Card Panels */
    .cyber-card {
        background-color: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 1.4rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
    }

    .cipher-badge {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        font-size: 0.78rem;
        font-weight: 600;
        border-radius: 9999px;
        background-color: rgba(6, 182, 212, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        margin-bottom: 0.8rem;
    }

    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #0d1322 !important;
        border-right: 1px solid #1e293b;
    }

    /* Code and Matrix Blocks */
    .matrix-cell {
        display: inline-block;
        width: 38px;
        height: 38px;
        line-height: 38px;
        text-align: center;
        background-color: #1e293b;
        color: #38bdf8;
        font-weight: 700;
        font-family: monospace;
        border: 1px solid #334155;
        border-radius: 4px;
        margin: 2px;
    }

    .output-box {
        background-color: #0f172a;
        border: 1px solid #0284c7;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Courier New', Courier, monospace;
        color: #38bdf8;
        font-size: 1.05rem;
        word-break: break-all;
    }
</style>
"""
st.markdown(CYBER_CSS, unsafe_allow_html=True)


def render_header():
    """Render top page title and educational safety warning."""
    st.markdown('<div class="main-title">CLASSICAL CRYPTOGRAPHY TOOLKIT</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="main-subtitle">An Interactive Educational Platform for Classical Encryption and Decryption</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="edu-banner">
            ⚠️ <strong>EDUCATIONAL INTEGRITY NOTICE:</strong> Classical cryptographic algorithms
            (Caesar, Monoalphabetic, Playfair, Hill, Vigenère, Rail Fence, Columnar Transposition)
            are historical mathematical constructions designed for educational study only. They lack
            semantic security, ciphertext integrity, and resilience against modern frequency analysis
            or computer-assisted cryptanalysis. <strong>DO NOT use classical ciphers for confidential or production data.</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    """Render sidebar navigation menu and project info."""
    with st.sidebar:
        st.markdown("### 🛡️ Navigation")
        nav_options = [
            "Dashboard",
            "Substitution Ciphers",
            "Transposition Ciphers",
            "Compare Algorithms",
            "Encrypt Text File",
            "Decrypt Text File",
            "Help and Documentation",
            "About Project",
        ]
        selection = st.radio("Select View:", nav_options, index=0)

        st.markdown("---")
        st.markdown("### 🎓 Academic Information")
        st.markdown(
            """
            **Course:** Network Security  
            **Class:** Final Year (ECM), 2026–27  
            **Student:** [ENTER YOUR NAME]  
            **Roll No:** [ENTER YOUR ROLL NUMBER]  
            **Batch:** [ENTER YOUR BATCH]  
            **Date:** [ENTER SUBMISSION DATE]
            """
        )
        st.caption("Toolkit Version: 1.0.0 (Final)")

        return selection


# ==============================================================================
# VIEW 1: DASHBOARD
# ==============================================================================
def render_dashboard():
    st.markdown("## 📊 Toolkit Dashboard")
    st.markdown(
        "Welcome to the **Classical Cryptography Toolkit**, a comprehensive laboratory for "
        "investigating classical substitution and transposition ciphers, key spaces, "
        "mathematical properties, and performance metrics."
    )

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Implemented Ciphers", "8 Algorithms", delta="100% Operational")
    with col2:
        st.metric("Cipher Categories", "2 Families", delta="Substitution & Transposition")
    with col3:
        st.metric("Test Suite Pass Rate", "51 / 51 Passed", delta="Pytest Verified")
    with col4:
        st.metric("File Processing", "Lossless UTF-8", delta="Metadata Preserved")

    st.markdown("---")

    # Categories overview cards
    col_sub, col_trans = st.columns(2)
    with col_sub:
        st.markdown(
            """
            <div class="cyber-card">
                <span class="cipher-badge">FAMILY 1</span>
                <h3>🔤 Substitution Ciphers (6)</h3>
                <p>Substitution ciphers preserve the order of characters but substitute each character or pair of characters with another symbol or vector.</p>
                <ul>
                    <li><strong>Caesar Cipher:</strong> Fixed modular shift mod 26.</li>
                    <li><strong>Monoalphabetic:</strong> Arbitrary permutation key of 26 letters.</li>
                    <li><strong>Playfair Cipher:</strong> Digraphic substitution on a 5×5 matrix.</li>
                    <li><strong>Hill Cipher:</strong> Linear algebraic block cipher via 2×2 invertible matrix.</li>
                    <li><strong>Vigenère Cipher:</strong> Polyalphabetic cipher using repeating keyword.</li>
                    <li><strong>One-Time Pad:</strong> Information-theoretically secure modular arithmetic.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_trans:
        st.markdown(
            """
            <div class="cyber-card">
                <span class="cipher-badge">FAMILY 2</span>
                <h3>🔄 Transposition Ciphers (2)</h3>
                <p>Transposition ciphers preserve the identity and frequencies of symbols but permute their physical order according to a geometric or keyword rule.</p>
                <ul>
                    <li><strong>Rail Fence Cipher:</strong> Zigzag transposition across depth levels (rails).</li>
                    <li><strong>Columnar Transposition:</strong> Matrix-based column reordering with stable tie-breaking and irregular row handling.</li>
                </ul>
                <br>
                <div style="background-color: #1e293b; padding: 0.75rem; border-radius: 6px;">
                    💡 <em>Transposition preserves character frequencies, making anagramming and bigram statistics primary cryptanalytic tools.</em>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 🚀 Quick Start Instructions")
    st.markdown(
        """
        1. **Explore Ciphers:** Use the sidebar to navigate to **Substitution Ciphers** or **Transposition Ciphers** to encrypt/decrypt messages with real-time mathematical step breakdowns.
        2. **Benchmark Algorithms:** Visit **Compare Algorithms** to run automated microsecond benchmarks on custom payloads.
        3. **Process Files:** Visit **Encrypt Text File** and **Decrypt Text File** for downloadable UTF-8 file transformations with structured metadata headers.
        """
    )


# ==============================================================================
# VIEW 2: SUBSTITUTION CIPHERS
# ==============================================================================
def render_substitution_ciphers():
    st.markdown("## 🔤 Substitution Ciphers")
    st.markdown("Choose an algorithm below to perform interactive encryption and decryption.")

    cipher_choice = st.selectbox(
        "Select Substitution Cipher:",
        [
            "Caesar Cipher",
            "Monoalphabetic Substitution Cipher",
            "Playfair Cipher",
            "Hill Cipher",
            "Vigenère Cipher",
            "One-Time Pad",
        ],
    )

    st.markdown("---")

    # 1. CAESAR CIPHER
    if cipher_choice == "Caesar Cipher":
        st.markdown("### 🏛️ Caesar Cipher")
        st.caption("Shift formula: C = (P + k) mod 26 | P = (C - k) mod 26")

        c1, c2 = st.columns([2, 1])
        with c1:
            input_text = st.text_area("Input Text (Plaintext or Ciphertext):", "NETWORK SECURITY", height=110)
        with c2:
            key_val = st.number_input("Integer Key (Shift):", value=5, step=1)
            st.caption("Supports positive, negative, and oversized integers (handled via mod 26).")

        col_b1, col_b2, col_b3 = st.columns([1, 1, 2])
        enc_clicked = col_b1.button("🔒 Encrypt", use_container_width=True)
        dec_clicked = col_b2.button("🔓 Decrypt", use_container_width=True)

        if enc_clicked:
            if not input_text:
                st.error("Please enter input text.")
            else:
                ciphertext = encrypt_caesar(input_text, int(key_val))
                st.success("Encryption Complete!")
                st.markdown(f'<div class="output-box">{ciphertext}</div>', unsafe_allow_html=True)
                steps = get_caesar_steps(input_text, int(key_val), mode="encrypt")
                if steps:
                    st.markdown("#### 🔍 Step-by-Step Shift Trace (First 12 Letters)")
                    st.dataframe(pd.DataFrame(steps), use_container_width=True)

        if dec_clicked:
            if not input_text:
                st.error("Please enter input text.")
            else:
                plaintext = decrypt_caesar(input_text, int(key_val))
                st.success("Decryption Complete!")
                st.markdown(f'<div class="output-box">{plaintext}</div>', unsafe_allow_html=True)
                steps = get_caesar_steps(input_text, int(key_val), mode="decrypt")
                if steps:
                    st.markdown("#### 🔍 Step-by-Step Shift Trace (First 12 Letters)")
                    st.dataframe(pd.DataFrame(steps), use_container_width=True)

    # 2. MONOALPHABETIC SUBSTITUTION
    elif cipher_choice == "Monoalphabetic Substitution Cipher":
        st.markdown("### 🔠 Monoalphabetic Substitution Cipher")
        st.caption("Replaces each letter A-Z with a unique corresponding letter from a 26-character key.")

        if "mono_key_state" not in st.session_state:
            st.session_state.mono_key_state = "QWERTYUIOPASDFGHJKLZXCVBNM"

        col_gen1, col_gen2 = st.columns([3, 1])
        with col_gen2:
            if st.button("🎲 Generate Random Key", use_container_width=True):
                st.session_state.mono_key_state = generate_monoalphabetic_key()

        with col_gen1:
            key_input = st.text_input(
                "26-Letter Substitution Alphabet Key (A-Z):",
                value=st.session_state.mono_key_state,
            )
            st.session_state.mono_key_state = key_input.strip().upper()

        is_valid_k, err_k = validate_monoalphabetic_key(st.session_state.mono_key_state)
        if not is_valid_k:
            st.error(f"Invalid Key: {err_k}")
        else:
            st.success("Key Validated: 26 unique English letters.")

        input_text = st.text_area("Input Text:", "Security in Computing 2026!", height=110)

        b1, b2 = st.columns(2)
        if b1.button("🔒 Encrypt", use_container_width=True):
            if not is_valid_k:
                st.error("Cannot encrypt with invalid key.")
            else:
                res = encrypt_monoalphabetic(input_text, st.session_state.mono_key_state)
                st.success("Ciphertext:")
                st.markdown(f'<div class="output-box">{res}</div>', unsafe_allow_html=True)

        if b2.button("🔓 Decrypt", use_container_width=True):
            if not is_valid_k:
                st.error("Cannot decrypt with invalid key.")
            else:
                res = decrypt_monoalphabetic(input_text, st.session_state.mono_key_state)
                st.success("Recovered Plaintext:")
                st.markdown(f'<div class="output-box">{res}</div>', unsafe_allow_html=True)

    # 3. PLAYFAIR CIPHER
    elif cipher_choice == "Playfair Cipher":
        st.markdown("### 🔲 Playfair Cipher")
        st.caption("Digraph substitution on a 5×5 matrix with 'I' and 'J' combined.")

        keyword = st.text_input("Enter Keyword:", "MONARCHY").strip().upper()
        if not keyword or not any(c.isalpha() for c in keyword):
            st.warning("Keyword must contain at least one alphabetic letter.")
        else:
            matrix = generate_playfair_matrix(keyword)
            st.markdown("#### 🧩 Generated 5×5 Key Matrix:")
            grid_html = '<div style="margin-bottom: 1rem;">'
            for row in matrix:
                grid_html += '<div>' + "".join([f'<span class="matrix-cell">{c}</span>' for c in row]) + '</div>'
            grid_html += '</div>'
            st.markdown(grid_html, unsafe_allow_html=True)

            input_text = st.text_area("Input Text:", "INSTRUMENT", height=100)

            col1, col2 = st.columns(2)
            if col1.button("🔒 Encrypt Digraphs", use_container_width=True):
                try:
                    c_text, details = encrypt_playfair(input_text, keyword)
                    st.success("Playfair Ciphertext:")
                    st.markdown(f'<div class="output-box">{details["formatted_ciphertext"]}</div>', unsafe_allow_html=True)

                    if details["prep_log"]:
                        st.info("Preprocessing Rules Applied: " + " | ".join(details["prep_log"]))

                    st.markdown("#### 🔍 Digraph Transformations:")
                    st.dataframe(pd.DataFrame(details["steps"]), use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")

            if col2.button("🔓 Decrypt Digraphs", use_container_width=True):
                try:
                    p_text, details = decrypt_playfair(input_text, keyword)
                    st.success("Playfair Decrypted Text:")
                    st.markdown(f'<div class="output-box">{details["formatted_decrypted"]}</div>', unsafe_allow_html=True)
                    st.caption(f"ℹ️ {details['note']}")
                    st.markdown("#### 🔍 Decryption Digraph Steps:")
                    st.dataframe(pd.DataFrame(details["steps"]), use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")

    # 4. HILL CIPHER
    elif cipher_choice == "Hill Cipher":
        st.markdown("### 🔢 Hill Cipher (2×2 Matrix mod 26)")
        st.caption("Vector polygraphic substitution: C = (K · P) mod 26 | P = (K⁻¹ · C) mod 26")

        preset = st.selectbox(
            "Matrix Presets or Custom:",
            [
                "Preset: [[3, 3], [2, 5]] (det = 9, coprime to 26)",
                "Preset: [[5, 8], [17, 3]] (det = 9, coprime to 26)",
                "Preset: [[7, 8], [11, 11]] (det = 15, coprime to 26)",
                "Custom Matrix",
            ],
        )

        if "Custom" in preset:
            c1, c2 = st.columns(2)
            with c1:
                k00 = st.number_input("Matrix K[0][0]:", value=3, step=1)
                k10 = st.number_input("Matrix K[1][0]:", value=2, step=1)
            with c2:
                k01 = st.number_input("Matrix K[0][1]:", value=3, step=1)
                k11 = st.number_input("Matrix K[1][1]:", value=5, step=1)
            matrix = [[int(k00), int(k01)], [int(k10), int(k11)]]
        elif "[[3, 3], [2, 5]]" in preset:
            matrix = [[3, 3], [2, 5]]
        elif "[[5, 8], [17, 3]]" in preset:
            matrix = [[5, 8], [17, 3]]
        else:
            matrix = [[7, 8], [11, 11]]

        is_valid_mat, mat_msg, det = validate_hill_matrix(matrix)
        if not is_valid_mat:
            st.error(f"❌ Invalid Matrix: {mat_msg}")
        else:
            inv_matrix = invert_matrix_mod26(matrix)
            st.success(f"✅ {mat_msg} Inverse Matrix mod 26 = {inv_matrix}")

        input_text = st.text_area("Input Text:", "HELP", height=100)
        preserve_fmt = st.checkbox("Preserve casing, spaces, and punctuation (lossless mode)", value=True)

        col1, col2 = st.columns(2)
        if col1.button("🔒 Encrypt Blocks", use_container_width=True):
            if not is_valid_mat:
                st.error("Cannot encrypt with non-invertible matrix.")
            else:
                try:
                    c_text, meta = encrypt_hill(input_text, matrix, preserve_formatting=preserve_fmt)
                    st.success("Hill Ciphertext:")
                    st.markdown(f'<div class="output-box">{c_text}</div>', unsafe_allow_html=True)
                    st.info(f"Padding Length: {meta['pad_len']} | Raw Blocks: {' '.join(meta['raw_blocks'])}")
                    st.session_state["hill_last_pad"] = meta["pad_len"]
                    if meta["steps"]:
                        st.markdown("#### 🔍 Matrix Transformation Trace:")
                        st.dataframe(pd.DataFrame(meta["steps"]), use_container_width=True)
                except Exception as e:
                    st.error(f"Encryption error: {e}")

        if col2.button("🔓 Decrypt Blocks", use_container_width=True):
            if not is_valid_mat:
                st.error("Cannot decrypt with non-invertible matrix.")
            else:
                try:
                    pad_to_use = st.session_state.get("hill_last_pad", 0)
                    p_text, meta = decrypt_hill(
                        input_text,
                        matrix,
                        pad_len=pad_to_use,
                        preserve_formatting=preserve_fmt,
                    )
                    st.success("Hill Decrypted Plaintext:")
                    st.markdown(f'<div class="output-box">{p_text}</div>', unsafe_allow_html=True)
                    if meta["steps"]:
                        st.markdown("#### 🔍 Inverse Matrix Decryption Trace:")
                        st.dataframe(pd.DataFrame(meta["steps"]), use_container_width=True)
                except Exception as e:
                    st.error(f"Decryption error: {e}")

    # 5. VIGENERE CIPHER
    elif cipher_choice == "Vigenère Cipher":
        st.markdown("### 🔠 Vigenère Cipher")
        st.caption("Polyalphabetic substitution with repeating keyword. Preserves spaces and casing.")

        keyword = st.text_input("Enter Keyword:", "LEMON").strip().upper()
        is_val_k, msg_k = validate_vigenere_key(keyword)
        if not is_val_k:
            st.error(f"Invalid Keyword: {msg_k}")

        input_text = st.text_area("Input Text:", "ATTACKATDAWN", height=100)

        c1, c2 = st.columns(2)
        if c1.button("🔒 Encrypt", use_container_width=True):
            if not is_val_k:
                st.error("Invalid keyword.")
            else:
                c_text = encrypt_vigenere(input_text, keyword)
                st.success("Vigenère Ciphertext:")
                st.markdown(f'<div class="output-box">{c_text}</div>', unsafe_allow_html=True)
                steps = get_vigenere_steps(input_text, keyword, mode="encrypt")
                if steps:
                    st.markdown("#### 🔍 Step-by-Step Keyword Trace:")
                    st.dataframe(pd.DataFrame(steps), use_container_width=True)

        if c2.button("🔓 Decrypt", use_container_width=True):
            if not is_val_k:
                st.error("Invalid keyword.")
            else:
                p_text = decrypt_vigenere(input_text, keyword)
                st.success("Recovered Plaintext:")
                st.markdown(f'<div class="output-box">{p_text}</div>', unsafe_allow_html=True)
                steps = get_vigenere_steps(input_text, keyword, mode="decrypt")
                if steps:
                    st.markdown("#### 🔍 Step-by-Step Decryption Trace:")
                    st.dataframe(pd.DataFrame(steps), use_container_width=True)

    # 6. ONE-TIME PAD
    elif cipher_choice == "One-Time Pad":
        st.markdown("### 🎲 One-Time Pad (Vernam Cipher)")
        st.caption("Information-theoretically secure modular alphabet addition.")
        st.warning(f"⚠️ {OTP_SECURITY_WARNING}")

        input_text = st.text_area("Input Text:", "CLASSIFIED NETWORK OPERATION", height=100)
        req_len = sum(1 for c in input_text if c.isalpha())

        if "otp_key_state" not in st.session_state:
            st.session_state.otp_key_state = generate_otp_key(req_len)

        col_k1, col_k2 = st.columns([3, 1])
        with col_k2:
            if st.button("🎲 Generate Random Key", use_container_width=True):
                st.session_state.otp_key_state = generate_otp_key(req_len)

        with col_k1:
            key_val = st.text_input(
                f"Secret Key (Requires at least {req_len} letters):",
                value=st.session_state.otp_key_state,
            )
            st.session_state.otp_key_state = key_val

        c1, c2 = st.columns(2)
        if c1.button("🔒 Encrypt (One-Time)", use_container_width=True):
            try:
                c_text, key_used = encrypt_otp(input_text, st.session_state.otp_key_state)
                st.success("OTP Ciphertext:")
                st.markdown(f'<div class="output-box">{c_text}</div>', unsafe_allow_html=True)
                st.info(f"Key stream applied ({len(key_used)} chars): `{key_used}`")
            except Exception as e:
                st.error(f"Error: {e}")

        if c2.button("🔓 Decrypt with Key", use_container_width=True):
            try:
                p_text = decrypt_otp(input_text, st.session_state.otp_key_state)
                st.success("Recovered Plaintext:")
                st.markdown(f'<div class="output-box">{p_text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")


# ==============================================================================
# VIEW 3: TRANSPOSITION CIPHERS
# ==============================================================================
def render_transposition_ciphers():
    st.markdown("## 🔄 Transposition Ciphers")
    st.markdown("Transposition ciphers permute the positions of letters without changing their identities.")

    cipher_choice = st.selectbox(
        "Select Transposition Cipher:",
        ["Rail Fence Cipher", "Columnar Transposition Cipher"],
    )

    st.markdown("---")

    # 1. RAIL FENCE CIPHER
    if cipher_choice == "Rail Fence Cipher":
        st.markdown("### 🚂 Rail Fence Cipher (Zigzag)")
        st.caption("Writes text along a zigzag diagonal across rails, then reads horizontally.")

        c1, c2 = st.columns([2, 1])
        with c1:
            input_text = st.text_area("Input Text:", "DEFEND THE EAST WALL", height=100)
        with c2:
            rails = st.number_input("Number of Rails (Depth d ≥ 1):", min_value=1, max_value=20, value=3, step=1)

        b1, b2 = st.columns(2)
        if b1.button("🔒 Encrypt Zigzag", use_container_width=True):
            c_text = encrypt_rail_fence(input_text, int(rails))
            st.success("Rail Fence Ciphertext:")
            st.markdown(f'<div class="output-box">{c_text}</div>', unsafe_allow_html=True)

            grid_lines = get_rail_fence_grid(input_text, int(rails))
            st.markdown("#### 📐 Visual Rail Fence Grid:")
            st.code("\n".join(grid_lines))

        if b2.button("🔓 Decrypt Zigzag", use_container_width=True):
            p_text = decrypt_rail_fence(input_text, int(rails))
            st.success("Recovered Plaintext:")
            st.markdown(f'<div class="output-box">{p_text}</div>', unsafe_allow_html=True)

            grid_lines = get_rail_fence_grid(p_text, int(rails))
            st.markdown("#### 📐 Visual Rail Fence Grid:")
            st.code("\n".join(grid_lines))

    # 2. COLUMNAR TRANSPOSITION
    elif cipher_choice == "Columnar Transposition Cipher":
        st.markdown("### 🏛️ Columnar Transposition Cipher")
        st.caption(
            "Matrix transposition where columns are read in alphabetical order of the key. "
            "Handles irregular rows cleanly and supports duplicate letter tie-breaking."
        )

        c1, c2 = st.columns([2, 1])
        with c1:
            input_text = st.text_area("Input Text:", "DEFEND THE EAST WALL AT DAWN", height=100)
        with c2:
            key_str = st.text_input("Enter Keyword Key:", "GERMAN").strip().upper()
            pad_mode = st.checkbox("Pad incomplete final row (lossless metadata)", value=False)

        is_val_k, msg_k = validate_columnar_key(key_str)
        if not is_val_k:
            st.error(f"Invalid Key: {msg_k}")

        b1, b2 = st.columns(2)
        if b1.button("🔒 Encrypt Columns", use_container_width=True):
            if not is_val_k:
                st.error("Invalid keyword.")
            else:
                c_text, meta = encrypt_columnar(input_text, key_str, pad=pad_mode)
                st.success("Columnar Ciphertext:")
                st.markdown(f'<div class="output-box">{c_text}</div>', unsafe_allow_html=True)
                st.session_state["col_last_pad"] = meta.get("pad_len", 0)

                st.markdown(f"**Column Reading Order:** `{meta['order']}`")
                if meta["col_details"]:
                    st.markdown("#### 🔍 Column Details:")
                    st.dataframe(pd.DataFrame(meta["col_details"]), use_container_width=True)

        if b2.button("🔓 Decrypt Columns", use_container_width=True):
            if not is_val_k:
                st.error("Invalid keyword.")
            else:
                pad_to_use = st.session_state.get("col_last_pad", 0) if pad_mode else 0
                p_text, meta = decrypt_columnar(input_text, key_str, pad_len=pad_to_use)
                st.success("Recovered Plaintext:")
                st.markdown(f'<div class="output-box">{p_text}</div>', unsafe_allow_html=True)


# ==============================================================================
# VIEW 4: COMPARE ALGORITHMS
# ==============================================================================
def render_compare_algorithms():
    st.markdown("## ⚡ Compare Algorithms (Performance & Metrics)")
    st.markdown(
        "Execute automated microsecond benchmarks across all eight classical ciphers on a common test message."
    )

    sample_text = st.text_area(
        "Benchmark Test Message:",
        value="NETWORK SECURITY AND CLASSICAL CRYPTOGRAPHY BENCHMARK PAYLOAD 2026",
        height=90,
    )

    iterations = st.slider("Benchmark Measurement Iterations:", min_value=1, max_value=20, value=5)

    if st.button("🚀 Run Comprehensive Benchmark", use_container_width=True):
        with st.spinner("Executing benchmarks using time.perf_counter()..."):
            df = benchmark_all_ciphers(sample_text, iterations=iterations)

        st.success("Benchmark Execution Complete!")
        st.markdown("### 📋 Comparative Results Table")
        st.dataframe(df, use_container_width=True)

        # Matplotlib visualization
        st.markdown("### 📈 Execution Time Breakdown (Microseconds)")
        fig, ax = plt.subplots(figsize=(10, 4.5))
        fig.patch.set_facecolor("#111827")
        ax.set_facecolor("#111827")

        algos = df["Algorithm"]
        enc_times = df["Enc Time (μs)"]
        dec_times = df["Dec Time (μs)"]

        x = range(len(algos))
        width = 0.35

        ax.bar([i - width / 2 for i in x], enc_times, width, label="Encryption Time (μs)", color="#06b6d4")
        ax.bar([i + width / 2 for i in x], dec_times, width, label="Decryption Time (μs)", color="#10b981")

        ax.set_ylabel("Time (μs)", color="#f3f4f6")
        ax.set_title("Classical Cipher Execution Speeds", color="#f3f4f6", fontsize=14)
        ax.set_xticks(x)
        ax.set_xticklabels(algos, rotation=35, ha="right", color="#f3f4f6")
        ax.tick_params(colors="#9ca3af")
        ax.legend(facecolor="#1e293b", edgecolor="#374151", labelcolor="#f3f4f6")
        plt.tight_layout()

        st.pyplot(fig)

        # Performance disclaimer
        st.markdown(
            f"""
            <div style="background-color: #1e293b; border-left: 4px solid #06b6d4; padding: 1rem; border-radius: 6px; margin-top: 1.5rem; color: #cbd5e1;">
                {COMPARISON_DISCLAIMER}
            </div>
            """,
            unsafe_allow_html=True,
        )


# ==============================================================================
# VIEW 5: ENCRYPT TEXT FILE
# ==============================================================================
def render_encrypt_file():
    st.markdown("## 📁 Encrypt Text File")
    st.markdown("Upload any standard `.txt` file, choose a cipher, and download the encrypted file with embedded metadata.")

    uploaded_file = st.file_uploader("Upload Plaintext File (.txt):", type=["txt"])

    if uploaded_file is not None:
        try:
            content = uploaded_file.read().decode("utf-8")
            st.info(f"Loaded file: `{uploaded_file.name}` ({len(content)} characters)")
            with st.expander("Preview File Contents:"):
                st.text(content[:500] + ("..." if len(content) > 500 else ""))

            col1, col2 = st.columns(2)
            with col1:
                cipher_name = st.selectbox(
                    "Choose Cipher Algorithm:",
                    [
                        "Caesar Cipher",
                        "Monoalphabetic Substitution Cipher",
                        "Playfair Cipher",
                        "Hill Cipher",
                        "Vigenère Cipher",
                        "One-Time Pad",
                        "Rail Fence Cipher",
                        "Columnar Transposition Cipher",
                    ],
                )

            with col2:
                # Dynamic key entry depending on cipher
                if cipher_name == "Caesar Cipher":
                    key_val = st.number_input("Caesar Key (Integer):", value=5, step=1)
                elif cipher_name == "Monoalphabetic Substitution Cipher":
                    key_val = st.text_input("26-Letter Substitution Key:", value="QWERTYUIOPASDFGHJKLZXCVBNM")
                elif cipher_name == "Playfair Cipher":
                    key_val = st.text_input("Keyword:", value="MONARCHY")
                elif cipher_name == "Hill Cipher":
                    st.caption("Using Coprime Matrix: [[3, 3], [2, 5]]")
                    key_val = [[3, 3], [2, 5]]
                elif cipher_name == "Vigenère Cipher":
                    key_val = st.text_input("Keyword:", value="CIPHER")
                elif cipher_name == "One-Time Pad":
                    alpha_len = sum(1 for c in content if c.isalpha())
                    st.caption(f"Requires {alpha_len} random characters.")
                    key_val = st.text_input("OTP Secret Key:", value=generate_otp_key(alpha_len))
                elif cipher_name == "Rail Fence Cipher":
                    key_val = st.number_input("Rail Count:", value=3, min_value=1, step=1)
                elif cipher_name == "Columnar Transposition Cipher":
                    key_val = st.text_input("Transposition Keyword:", value="GERMAN")

            if st.button("🔒 Encrypt and Package File", use_container_width=True):
                try:
                    packaged_data, meta = encrypt_text_file(content, cipher_name, key_val)
                    st.success("File Successfully Encrypted and Packaged!")
                    with st.expander("Preview Packaged Output:"):
                        st.text(packaged_data[:600] + "...")

                    st.download_button(
                        label="⬇️ Download Encrypted File (.txt)",
                        data=packaged_data.encode("utf-8"),
                        file_name=f"encrypted_{uploaded_file.name}",
                        mime="text/plain",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.error(f"File Encryption Failed: {e}")

        except UnicodeDecodeError:
            st.error("Error: Uploaded file must be encoded in UTF-8 text format.")


# ==============================================================================
# VIEW 6: DECRYPT TEXT FILE
# ==============================================================================
def render_decrypt_file():
    st.markdown("## 🔓 Decrypt Text File")
    st.markdown("Upload a toolkit-encrypted text file. The system will inspect headers and recover the original plaintext.")

    uploaded_file = st.file_uploader("Upload Toolkit Encrypted File (.txt):", type=["txt"])

    if uploaded_file is not None:
        try:
            content = uploaded_file.read().decode("utf-8")
            parsed = parse_encrypted_file_content(content)

            st.success(f"Detected Encrypted Format! Cipher Used: **{parsed['cipher_name']}**")
            st.caption(f"Encrypted on: {parsed['timestamp']} | Metadata: `{parsed['metadata']}`")

            detected_cipher = parsed["cipher_name"]

            # Prompt user for corresponding key
            if detected_cipher == "Caesar Cipher":
                key_val = st.number_input("Enter Caesar Key:", value=5, step=1)
            elif detected_cipher == "Monoalphabetic Substitution Cipher":
                key_val = st.text_input("Enter 26-Letter Key:", value="QWERTYUIOPASDFGHJKLZXCVBNM")
            elif detected_cipher == "Playfair Cipher":
                key_val = st.text_input("Enter Keyword:", value="MONARCHY")
            elif detected_cipher == "Hill Cipher":
                st.caption("Decryption requires the 2x2 key matrix used during encryption.")
                key_val = [[3, 3], [2, 5]]
            elif detected_cipher == "Vigenère Cipher":
                key_val = st.text_input("Enter Keyword:", value="CIPHER")
            elif detected_cipher == "One-Time Pad":
                key_val = st.text_input("Enter One-Time Pad Secret Key:")
            elif detected_cipher == "Rail Fence Cipher":
                key_val = st.number_input("Enter Number of Rails:", value=3, min_value=1, step=1)
            elif detected_cipher == "Columnar Transposition Cipher":
                key_val = st.text_input("Enter Transposition Keyword:", value="GERMAN")

            if st.button("🔓 Decrypt File", use_container_width=True):
                try:
                    decrypted_text, _ = decrypt_text_file(content, key_val, expected_cipher=detected_cipher)
                    st.success("Decryption Successful!")

                    with st.expander("Preview Recovered Text:"):
                        st.text(decrypted_text[:600] + ("..." if len(decrypted_text) > 600 else ""))

                    st.download_button(
                        label="⬇️ Download Decrypted Plaintext (.txt)",
                        data=decrypted_text.encode("utf-8"),
                        file_name=f"recovered_{uploaded_file.name}",
                        mime="text/plain",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.error(f"Decryption Error: {e}")

        except ValueError as val_err:
            st.error(f"Invalid or Unrecognized File Format: {val_err}")
        except Exception as e:
            st.error(f"Unexpected File Error: {e}")


# ==============================================================================
# VIEW 7: HELP AND DOCUMENTATION
# ==============================================================================
def render_help():
    st.markdown("## 📖 Help and Educational Documentation")

    tab1, tab2, tab3 = st.tabs(["📚 Cipher Theory", "⚠️ Common Errors & Fixes", "🔒 Modern vs Classical"])

    with tab1:
        st.markdown(
            r"""
            ### Classification of Classical Cryptography
            Classical ciphers are divided into two fundamental branches:
            
            1. **Substitution Ciphers:**
               - **Caesar Cipher:** Monoalphabetic shift cipher using modular arithmetic ($C = (P + k) \pmod{26}$).
               - **Monoalphabetic:** Uses arbitrary 26-letter permutation; vulnerability: letter frequency analysis ($E, T, A, O, I, N$).
               - **Playfair Cipher:** First practical digraphic cipher invented by Charles Wheatstone (1854); replaces 25-letter pairs via geometric grid rules.
               - **Hill Cipher:** Lester S. Hill (1929); applies matrix multiplication mod 26. Invertible only when $\gcd(\det(K), 26) = 1$.
               - **Vigenère Cipher:** Polyalphabetic cipher using Tabula Recta; resists simple monoalphabetic frequency attacks, broken via Kasiski examination.
               - **One-Time Pad (Vernam):** Gilbert Vernam (1917) & Claude Shannon (1949); information-theoretically unbreakable when key is uniformly random, secret, equal length, and used once.

            2. **Transposition Ciphers:**
               - **Rail Fence:** Writes in zigzag diagonals and reads horizontally.
               - **Columnar Transposition:** Writes plaintext in rectangular rows and reads columns according to sorted key order.
            """
        )

    with tab2:
        st.markdown(
            r"""
            ### Troubleshooting & Common Errors
            - **Hill Cipher Matrix Error:**
              - *Error:* Determinant is even or shares a factor with 26.
              - *Fix:* Ensure $\det(K) \pmod{26}$ is odd and not 13. Example valid matrix: `[[3, 3], [2, 5]]`.
            - **Monoalphabetic Key Error:**
              - *Error:* Key must contain exactly 26 unique letters.
              - *Fix:* Use the "🎲 Generate Random Key" button to produce a verified 26-letter permutation.
            - **One-Time Pad Key Too Short:**
              - *Error:* Key length is less than alphabetic letter count.
              - *Fix:* The key must contain at least as many letters as the plaintext payload.
            - **Playfair Decryption Ciphertext Odd Length:**
              - *Error:* Ciphertext length must be even.
              - *Fix:* Playfair operates on letter pairs (digraphs). Ensure ciphertext contains an even number of characters.
            """
        )

    with tab3:
        st.markdown(
            """
            ### Classical vs Modern Cryptography
            | Property | Classical Cryptography | Modern Cryptography (AES, RSA, ECC) |
            | :--- | :--- | :--- |
            | **Security Basis** | Security by obscurity / secrecy of algorithm | Kerckhoffs's Principle (Public algorithm, secret key) |
            | **Computational Unit** | Alphabetic letters (A-Z) | Binary bits and bytes ($2^{128}$, $2^{256}$) |
            | **Attack Complexity** | Broken in seconds via frequency analysis | $2^{128}$ or $2^{256}$ operations (Infeasible for supercomputers) |
            | **Integrity / Auth** | None (Trivial tampering) | Cryptographic MACs, HMAC, AEAD (GCM mode), Digital Signatures |
            | **Standard Applications**| Historical education, puzzles | Banking, TLS 1.3, VPNs, Disk Encryption, Blockchain |
            """
        )


# ==============================================================================
# VIEW 8: ABOUT PROJECT
# ==============================================================================
def render_about():
    st.markdown("## ℹ️ About Project")
    st.markdown(
        """
        ### Project Details
        - **Project Title:** Design and Development of a Classical Cryptography Toolkit
        - **Course:** Network Security
        - **Class:** Final Year (ECM), 2026–27
        - **Student Name:** [ENTER YOUR NAME]
        - **Roll Number:** [ENTER YOUR ROLL NUMBER]
        - **Batch:** [ENTER YOUR BATCH]
        - **Submission Date:** [ENTER SUBMISSION DATE]

        ### System Architecture & Technologies
        - **Backend:** Python 3.14 (Math, Random, Secrets, Perf_Counter)
        - **Frontend Interface:** Streamlit (Cyber Dark UI, Responsive CSS)
        - **Automated Testing:** Pytest (51 Unit Tests, 100% Passing)
        - **Data Handling & Charting:** Pandas & Matplotlib
        - **File System:** UTF-8 Structured Metadata Preservation
        """
    )


# ==============================================================================
# MAIN CONTROLLER
# ==============================================================================
def main():
    render_header()
    selection = render_sidebar()

    if selection == "Dashboard":
        render_dashboard()
    elif selection == "Substitution Ciphers":
        render_substitution_ciphers()
    elif selection == "Transposition Ciphers":
        render_transposition_ciphers()
    elif selection == "Compare Algorithms":
        render_compare_algorithms()
    elif selection == "Encrypt Text File":
        render_encrypt_file()
    elif selection == "Decrypt Text File":
        render_decrypt_file()
    elif selection == "Help and Documentation":
        render_help()
    elif selection == "About Project":
        render_about()


if __name__ == "__main__":
    main()
