# 🔐 Hybrid File Encryption System (RSA + AES)

This project is a **hybrid encryption system** built with Python that securely encrypts and decrypts files using:

- **RSA (Asymmetric Encryption)** for key exchange  
- **AES (Fernet / Symmetric Encryption)** for fast and secure data encryption  

It demonstrates how modern secure systems protect data using both cryptography methods together.

---

## 🚀 How It Works

1. Generates an RSA public/private key pair  
2. Creates a random AES session key  
3. Encrypts the file using AES  
4. Encrypts the AES session key using RSA public key  
5. Stores both securely in a single encrypted file  
6. Uses the RSA private key to decrypt everything back safely  

---

## 🛠 Requirements

- Python 3.x  
- cryptography library  

Install requirements:

```bash
pip install cryptography
