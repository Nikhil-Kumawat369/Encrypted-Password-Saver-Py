# 🔐 Encrypted Password Saver (Python)

A secure, console-based encrypted data storage system built with Python.  
This project demonstrates real-world security concepts including password hashing, key derivation, and symmetric encryption.

---

## 🚀 Project Overview

The **Encrypted Password Saver** allows users to:

- Create secure accounts
- Log in using hashed passwords
- Store personal data in encrypted format
- Retrieve and decrypt stored data securely
- Clear stored data without deleting the account

The system ensures that:

- Passwords are never stored in plain text
- Encryption keys are derived securely
- User data cannot be accessed without proper authentication

---

## 🔐 Security Architecture

This project implements multiple layers of security:

### 1️⃣ Password Hashing (Authentication Layer)
- Uses **bcrypt**
- Passwords are hashed with a secure salt
- Original passwords are never stored
- Even the system cannot retrieve user passwords

### 2️⃣ Key Derivation (Cryptographic Key Generation)
- Uses **Scrypt KDF**
- Generates a unique encryption key from:
  - User password
  - Randomly generated salt
- Resistant to brute-force and GPU attacks

### 3️⃣ Data Encryption (Confidentiality Layer)
- Uses **Fernet (AES-based symmetric encryption)**
- User data is stored fully encrypted
- Data cannot be decrypted without:
  - Correct password
  - Correct salt
  - Correct derived key

---

## 🧠 How It Works

1. User signs up
2. Password is hashed using bcrypt
3. A random salt is generated
4. Encryption key is derived using Scrypt
5. User’s personal file is created
6. All stored content is encrypted using Fernet

On login:

- Password is verified using bcrypt
- Key is regenerated using stored salt
- Data is decrypted only after successful authentication

---

## 📁 Project Structure

    Encrypted-Password-Saver-Py/
    │
    ├── Database/
    │ ├── userNameDatabase.txt
    │ ├── userCredentials.txt
    │ ├──username.txt
    │
    └── main.py

---

## ✨ Features

- 🔐 Secure Sign Up & Login system
- 🔑 Strong password hashing (bcrypt)
- 🧬 Cryptographic key derivation (Scrypt)
- 🔒 Encrypted personal storage per user
- 🗂 Individual user files
- 🧹 Clear stored data option
- 🛡 Protection against plain-text password leaks

---

## ▶ How To Run

### 1. Install Dependencies

```bash
pip install bcrypt 
pip install cryptography
```

### 2. Run the Program

```python
python Main.py
```

## 📜 Usage Flow

### 1. Launch the program

### 2. Choose:

- Sign Up

- Log In

### 3. After login:

- Add encrypted data

- View decrypted data

- Clear all stored data

### 4. To finish adding data, type:

END

## 🧪 Security Challenge (Optional Feature)

This project can be used as a security challenge :

- Even if someone gains access to the database files , they cannot retrieve passwords or decrypt stored data without the correct credentials.

- You may create a test account and challenge others to:

Crack the hashed password

- Decrypt stored encrypted content

- Demonstrating the strength of modern cryptographic practices.

## 🏆 What This Project Demonstrates

- Understanding of hashing vs encryption

- Secure password storage principles

- Use of cryptographic key derivation functions

- File handling in binary mode

- Secure system design fundamentals

This is not just a beginner script — it is a foundational security project.


## 🔮 Future Improvements

- Add login attempt limiting

- Convert to JSON-based storage

- Add delete specific entry feature

- Implement password strength checker

- Add GUI (Tkinter / PyQt)

- Convert into web app (Flask / Django)

- Implement logging system

- Add multi-session handling

## ⚠ Disclaimer

This project is built for educational purposes.

While it implements strong cryptographic practices, it is not intended for production-level deployment without further hardening.

## 📜 License


>This project is open for learning and experimentation.
>You may modify, distribute, or expand it freely.


## 👤 Author


Developed by: Nikhil Kumawat
<br>
Language: Python
<br>
Project: Encrypted Password Saver

>“Security is not optional.”

## ⭐ Final Note

This project represents a major milestone in understanding authentication and encryption fundamentals.

If you are reading decrypted protected data without credentials — you truly earned respect.

>⭐ If you like this project, consider giving it a star!
