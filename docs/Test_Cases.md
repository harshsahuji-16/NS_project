# Automated Test Cases and Quality Assurance Report

**Course:** Network Security  
**Academic Year:** 2026–27 | **Class:** Final Year (ECM)  
**Project Title:** Design and Development of a Classical Cryptography Toolkit  
**Test Framework:** Pytest 9.1.1 on Python 3.14  
**Total Tests Executed:** 51  
**Total Tests Passed:** 51  
**Total Tests Failed:** 0  
**Pass Rate:** 100.0%  
**Execution Runtime:** 0.77 seconds  

---

## 1. Summary Test Execution Table

| Test ID | Module | Test Function Name | Description / Scenario | Input Data & Keys | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | `test_caesar.py` | `test_caesar_reference_test_case` | Known prompt reference vector | Text: `"NETWORK SECURITY"`, Key: `5` | Cipher: `"SJYBTWP XJHZWNYD"`, Decrypt: `"NETWORK SECURITY"` | Matched exact reference string | **PASSED** |
| **TC-02** | `test_caesar.py` | `test_caesar_case_and_punctuation_preservation` | Mixed case, spaces, symbols | Text: `"Hello, World! 123"`, Key: `3` | Cipher: `"Khoor, Zruog! 123"`, Decrypt: `"Hello, World! 123"` | Matched exact format | **PASSED** |
| **TC-03** | `test_caesar.py` | `test_caesar_negative_and_oversized_keys` | Modulo 26 boundary arithmetic | Text: `"Cryptography"`, Keys: `3, 29, -23` | All produce identical ciphertext; reversible | All matched identical ciphertext | **PASSED** |
| **TC-04** | `test_caesar.py` | `test_caesar_empty_string` | Empty string input | Text: `""`, Key: `7` | Return empty string `""` | Returned `""` | **PASSED** |
| **TC-05** | `test_caesar.py` | `test_caesar_zero_key` | Shift of zero (identity transformation) | Text: `"Secret Message"`, Key: `0` | Return text unchanged | Returned text unchanged | **PASSED** |
| **TC-06** | `test_caesar.py` | `test_caesar_invalid_key_type` | Type validation | Key: `"invalid"`, `3.14` | Raise `TypeError` | Raised `TypeError` | **PASSED** |
| **TC-07** | `test_caesar.py` | `test_caesar_steps_generation` | Step-by-step trace generator | Text: `"ABC"`, Key: `3` | 3 step dicts with formulas | Generated accurate trace | **PASSED** |
| **TC-08** | `test_monoalphabetic.py` | `test_monoalphabetic_key_generation` | Random 26-letter key generator | Call `generate_monoalphabetic_key()` | 26 unique uppercase letters | 26 unique A-Z characters | **PASSED** |
| **TC-09** | `test_monoalphabetic.py` | `test_monoalphabetic_round_trip` | Lossless encryption & decryption | Key: QWERTY..., Text: `"Network Security Mini Project 2026!"` | Plaintext matches decrypted string | Exact match | **PASSED** |
| **TC-10** | `test_monoalphabetic.py` | `test_monoalphabetic_case_preservation` | Upper/lower casing preservation | Text: `"AbC, xYz!"`, Key: QWERTY... | Cipher: `"QwE, bNm!"`, Decrypt: `"AbC, xYz!"` | Exact match | **PASSED** |
| **TC-11** | `test_monoalphabetic.py` | `test_monoalphabetic_invalid_keys` | Rejection of bad keys | Keys: `"ABC"`, `"A"*26`, with numbers | Return `(False, msg)` and raise `ValueError` | Rejected with descriptive errors | **PASSED** |
| **TC-12** | `test_monoalphabetic.py` | `test_monoalphabetic_empty_text` | Empty string input | Text: `""`, Key: QWERTY... | Return empty string `""` | Returned `""` | **PASSED** |
| **TC-13** | `test_playfair.py` | `test_playfair_matrix_generation` | 5x5 key matrix structure | Keyword: `"MONARCHY"` | 5x5 matrix, 'I' present, 'J' omitted, 25 unique | 5x5 grid with unique letters | **PASSED** |
| **TC-14** | `test_playfair.py` | `test_playfair_digraph_preprocessing` | Digraph pairing with fillers | Text: `"BALLOON"` | Pairs: `[('B','A'), ('L','X'), ('L','O'), ('O','N')]` | Exact digraph sequence | **PASSED** |
| **TC-15** | `test_playfair.py` | `test_playfair_known_text_encryption_and_decryption` | Textbook Playfair vector | Keyword: `"MONARCHY"`, Text: `"INSTRUMENT"` | Even length cipher, reversible digraphs | Reversible digraphs | **PASSED** |
| **TC-16** | `test_playfair.py` | `test_playfair_repeated_letter_filler` | Consecutive duplicate letters | Text: `"HELLO"`, Keyword: `"SECURITY"` | Decrypted digraphs retain filler: `"HELXLO"` | Returned `"HELXLO"` | **PASSED** |
| **TC-17** | `test_playfair.py` | `test_playfair_invalid_keyword` | Rejection of invalid keyword | Keyword: `"12345"`, `""` | Raise `ValueError` | Raised `ValueError` | **PASSED** |
| **TC-18** | `test_playfair.py` | `test_playfair_invalid_ciphertext_length` | Odd-length ciphertext rejection | Ciphertext: `"ABC"` (3 chars) | Raise `ValueError` | Raised `ValueError` | **PASSED** |
| **TC-19** | `test_hill.py` | `test_hill_matrix_validation_valid` | Valid coprime matrix validation | Matrix: `[[3, 3], [2, 5]]` | Det = 9, $\gcd(9, 26) = 1$, Return True | Accepted with Det=9 | **PASSED** |
| **TC-20** | `test_hill.py` | `test_hill_matrix_inversion` | Modular inverse matrix mod 26 | Matrix: `[[3, 3], [2, 5]]` | Inverse: `[[15, 17], [20, 9]]`, $K \cdot K^{-1} = I \pmod{26}$ | Exact inverse, $I$ verified | **PASSED** |
| **TC-21** | `test_hill.py` | `test_hill_known_text_encryption` | Textbook Hill Cipher example | Text: `"HELP"`, Key: `[[3, 3], [2, 5]]` | Cipher: `"HIAT"`, Decrypt: `"HELP"` | Exact `"HIAT"` and `"HELP"` | **PASSED** |
| **TC-22** | `test_hill.py` | `test_hill_padding_and_lossless_recovery` | Odd length padding with metadata | Text: `"DEF"`, Key: `[[3, 3], [2, 5]]` | `pad_len = 1`, round-trip dec recovers `"DEF"` | Exact `"DEF"` recovered | **PASSED** |
| **TC-23** | `test_hill.py` | `test_hill_case_and_punctuation_preservation` | Formatting preservation mode | Text: `"Network Security, 2026!"` | Plaintext matches decrypted string | Exact match | **PASSED** |
| **TC-24** | `test_hill.py` | `test_hill_invalid_matrix_singular` | Rejection of singular matrix | Matrix: `[[2, 4], [1, 2]]` (Det = 0) | Reject: Determinant is 0 mod 26 | Rejected with clear error | **PASSED** |
| **TC-25** | `test_hill.py` | `test_hill_invalid_matrix_even_determinant` | Rejection of even determinant | Matrix: `[[2, 1], [4, 3]]` (Det = 2) | Reject: Shares common factor 2 with 26 | Rejected with factor 2 notice | **PASSED** |
| **TC-26** | `test_hill.py` | `test_hill_invalid_matrix_factor_13` | Rejection of det sharing factor 13 | Matrix: `[[1, 0], [0, 13]]` (Det = 13) | Reject: Shares common factor 13 with 26 | Rejected with factor 13 notice | **PASSED** |
| **TC-27** | `test_hill.py` | `test_hill_invalid_dimensions` | Matrix dimension check | Non-2x2 matrix: `[[1, 2, 3]]` | Reject: Matrix must be 2x2 | Rejected | **PASSED** |
| **TC-28** | `test_vigenere.py` | `test_vigenere_known_text_reference` | Textbook polyalphabetic vector | Text: `"ATTACKATDAWN"`, Key: `"LEMON"` | Cipher: `"LXFOPVEFRNHR"`, Decrypt: `"ATTACKATDAWN"` | Exact match | **PASSED** |
| **TC-29** | `test_vigenere.py` | `test_vigenere_case_and_punctuation_preservation` | Key index preservation on non-letters | Text: `"Attack at Dawn, 0600!"`, Key: `"LEMON"` | Cipher: `"Lxfopv ef Rnhr, 0600!"`, Reversible | Exact match | **PASSED** |
| **TC-30** | `test_vigenere.py` | `test_vigenere_key_validation` | Keyword validation | Keys: `"SECRET"` (Valid), `"12345"` (Invalid) | Return `(True, "")` and `(False, msg)` | Validated accurately | **PASSED** |
| **TC-31** | `test_vigenere.py` | `test_vigenere_steps_generation` | Educational keyword trace | Text: `"ATTACK"`, Key: `"LEMON"` | 6 step dicts showing modular additions | Generated accurate steps | **PASSED** |
| **TC-32** | `test_one_time_pad.py` | `test_otp_key_generation` | Cryptographic random key gen | Length: `10` | 10-char uppercase string from `secrets` | Valid 10-char random key | **PASSED** |
| **TC-33** | `test_one_time_pad.py` | `test_otp_round_trip` | OTP round-trip encryption | Text: `"Network Security Final Year Project 2026!"` | Cipher != Plaintext, Decrypt == Plaintext | Exact match | **PASSED** |
| **TC-34** | `test_one_time_pad.py` | `test_otp_insufficient_key_length` | Short key rejection | Text: `"CONFIDENTIAL"`, Key: `"ABC"` | Raise `ValueError`: Key is too short | Raised `ValueError` | **PASSED** |
| **TC-35** | `test_one_time_pad.py` | `test_otp_warning_content` | Security notice presence | Inspect `OTP_SECURITY_WARNING` | Contains "NEVER reused" & "information-theoretically" | Confirmed present | **PASSED** |
| **TC-36** | `test_rail_fence.py` | `test_rail_fence_known_reference` | Textbook 3-rail zigzag vector | Text: `"DEFEND THE EAST WALL"`, Rails: `3` | Cipher != Plaintext, Decrypt == Plaintext | Exact match | **PASSED** |
| **TC-37** | `test_rail_fence.py` | `test_rail_fence_boundary_rails` | Boundary rail values | Text: `"SECURITY"`, Rails: `1`, `20` | Rails = 1 and Rails >= Len return text as-is | Returned text unchanged | **PASSED** |
| **TC-38** | `test_rail_fence.py` | `test_rail_fence_empty_string` | Empty string input | Text: `""`, Rails: `4` | Return empty string `""` | Returned `""` | **PASSED** |
| **TC-39** | `test_rail_fence.py` | `test_rail_fence_invalid_rails` | Rail validation | Rails: `0`, `-2` | Raise `ValueError` | Raised `ValueError` | **PASSED** |
| **TC-40** | `test_rail_fence.py` | `test_rail_fence_grid_helper` | Visual ascii grid generator | Text: `"HELLOWORLD"`, Rails: `3` | 3 string lines representing zigzag pattern | Generated valid grid | **PASSED** |
| **TC-41** | `test_columnar_transposition.py` | `test_columnar_key_order_and_duplicate_handling` | Stable sort tie breaking | Keyword: `"BALLOON"` | Read order: `[1, 0, 2, 3, 6, 4, 5]` | Exact index order | **PASSED** |
| **TC-42** | `test_columnar_transposition.py` | `test_columnar_irregular_transposition_round_trip` | Irregular uneven rows | Text: `"DEFEND THE EAST WALL AT DAWN!"`, Key: `"GERMAN"` | Reversible without padding (`pad_len = 0`) | Exact match | **PASSED** |
| **TC-43** | `test_columnar_transposition.py` | `test_columnar_padded_transposition_round_trip` | Padded transposition with metadata | Text: `"Network Security Mini Project"`, Key: `"CIPHER"` | Reversible using metadata `pad_len` | Exact match | **PASSED** |
| **TC-44** | `test_columnar_transposition.py` | `test_columnar_empty_text` | Empty string input | Text: `""`, Key: `"KEYWORD"` | Return empty string `""` | Returned `""` | **PASSED** |
| **TC-45** | `test_columnar_transposition.py` | `test_columnar_invalid_keys` | Key validation | Key: `"A"` (length < 2) | Raise `ValueError` | Raised `ValueError` | **PASSED** |
| **TC-46** | `test_file_handler.py` | `test_file_packaging_and_parsing` | File envelope formatting | Cipher: `"Caesar Cipher"`, Meta: `{"pad_len": 0}` | Structured header parseable into dict | Parsed header perfectly | **PASSED** |
| **TC-47** | `test_file_handler.py` | `test_file_encryption_decryption_caesar` | Multi-line file round-trip | Multi-line text with numbers and symbols | Reconstructed exact multi-line text | Exact match | **PASSED** |
| **TC-48** | `test_file_handler.py` | `test_file_encryption_decryption_hill_with_padding` | File encryption with Hill padding | Odd-length multi-line file, Key: `[[3, 3], [2, 5]]` | Metadata header preserves `pad_len`, lossless dec | Lossless recovery | **PASSED** |
| **TC-49** | `test_file_handler.py` | `test_file_handler_empty_content_rejection` | Empty file rejection | Empty string `""` | Raise `ValueError`: Cannot encrypt empty file | Raised `ValueError` | **PASSED** |
| **TC-50** | `test_file_handler.py` | `test_file_handler_corrupted_file_rejection` | Corrupted file rejection | Arbitrary text without `# CLASSICAL CRYPTOGRAPHY...` | Raise `ValueError`: Missing toolkit signature | Raised `ValueError` | **PASSED** |
| **TC-51** | `test_file_handler.py` | `test_file_handler_cipher_mismatch` | Cipher mismatch rejection | Encrypted with Caesar, decrypted as Vigenère | Raise `ValueError`: Cipher mismatch | Raised `ValueError` | **PASSED** |

---

## 2. Pytest Execution Console Transcript

```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\harsh\AppData\Local\Programs\Python\Python314\python.exe
cachedir: .pytest_cache
rootdir: E:\NS_P
plugins: anyio-4.15.1
collecting ... collected 51 items

tests/test_caesar.py::test_caesar_reference_test_case PASSED             [  1%]
tests/test_caesar.py::test_caesar_case_and_punctuation_preservation PASSED [  3%]
tests/test_caesar.py::test_caesar_negative_and_oversized_keys PASSED     [  5%]
tests/test_caesar.py::test_caesar_empty_string PASSED                    [  7%]
tests/test_caesar.py::test_caesar_zero_key PASSED                        [  9%]
tests/test_caesar.py::test_caesar_invalid_key_type PASSED                [ 11%]
tests/test_caesar.py::test_caesar_steps_generation PASSED                [ 13%]
tests/test_columnar_transposition.py::test_columnar_key_order_and_duplicate_handling PASSED [ 15%]
tests/test_columnar_transposition.py::test_columnar_irregular_transposition_round_trip PASSED [ 17%]
tests/test_columnar_transposition.py::test_columnar_padded_transposition_round_trip PASSED [ 19%]
tests/test_columnar_transposition.py::test_columnar_empty_text PASSED    [ 21%]
tests/test_columnar_transposition.py::test_columnar_invalid_keys PASSED  [ 23%]
tests/test_file_handler.py::test_file_packaging_and_parsing PASSED       [ 25%]
tests/test_file_handler.py::test_file_encryption_decryption_caesar PASSED [ 27%]
tests/test_file_handler.py::test_file_encryption_decryption_hill_with_padding PASSED [ 29%]
tests/test_file_handler.py::test_file_handler_empty_content_rejection PASSED [ 31%]
tests/test_file_handler.py::test_file_handler_corrupted_file_rejection PASSED [ 33%]
tests/test_file_handler.py::test_file_handler_cipher_mismatch PASSED     [ 35%]
tests/test_hill.py::test_hill_matrix_validation_valid PASSED             [ 37%]
tests/test_hill.py::test_hill_matrix_inversion PASSED                    [ 39%]
tests/test_hill.py::test_hill_known_text_encryption PASSED               [ 41%]
tests/test_hill.py::test_hill_padding_and_lossless_recovery PASSED       [ 43%]
tests/test_hill.py::test_hill_case_and_punctuation_preservation PASSED   [ 45%]
tests/test_hill.py::test_hill_invalid_matrix_singular PASSED             [ 47%]
tests/test_hill.py::test_hill_invalid_matrix_even_determinant PASSED     [ 49%]
tests/test_hill.py::test_hill_invalid_matrix_factor_13 PASSED            [ 50%]
tests/test_hill.py::test_hill_invalid_dimensions PASSED                  [ 52%]
tests/test_monoalphabetic.py::test_monoalphabetic_key_generation PASSED  [ 54%]
tests/test_monoalphabetic.py::test_monoalphabetic_round_trip PASSED      [ 56%]
tests/test_monoalphabetic.py::test_monoalphabetic_case_preservation PASSED [ 58%]
tests/test_monoalphabetic.py::test_monoalphabetic_invalid_keys PASSED    [ 60%]
tests/test_monoalphabetic.py::test_monoalphabetic_empty_text PASSED      [ 62%]
tests/test_one_time_pad.py::test_otp_key_generation PASSED               [ 64%]
tests/test_one_time_pad.py::test_otp_round_trip PASSED                   [ 66%]
tests/test_one_time_pad.py::test_otp_insufficient_key_length PASSED      [ 68%]
tests/test_one_time_pad.py::test_otp_warning_content PASSED              [ 70%]
tests/test_playfair.py::test_playfair_matrix_generation PASSED           [ 72%]
tests/test_playfair.py::test_playfair_digraph_preprocessing PASSED       [ 74%]
tests/test_playfair.py::test_playfair_known_text_encryption_and_decryption PASSED [ 76%]
tests/test_playfair.py::test_playfair_repeated_letter_filler PASSED      [ 78%]
tests/test_playfair.py::test_playfair_invalid_keyword PASSED             [ 80%]
tests/test_playfair.py::test_playfair_invalid_ciphertext_length PASSED   [ 82%]
tests/test_rail_fence.py::test_rail_fence_known_reference PASSED         [ 84%]
tests/test_rail_fence.py::test_rail_fence_boundary_rails PASSED          [ 86%]
tests/test_rail_fence.py::test_rail_fence_empty_string PASSED            [ 88%]
tests/test_rail_fence.py::test_rail_fence_invalid_rails PASSED           [ 90%]
tests/test_rail_fence.py::test_rail_fence_grid_helper PASSED             [ 92%]
tests/test_vigenere.py::test_vigenere_known_text_reference PASSED        [ 94%]
tests/test_vigenere.py::test_vigenere_case_and_punctuation_preservation PASSED [ 96%]
tests/test_vigenere.py::test_vigenere_key_validation PASSED              [ 98%]
tests/test_vigenere.py::test_vigenere_steps_generation PASSED            [100%]

============================= 51 passed in 0.77s ==============================
```
