import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.fernet import Fernet

def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    
    # Save Private Key
    with open("private.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
        
    # Save Public Key
    public_key = private_key.public_key()
    with open("public.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    print("Keys generated: private.pem and public.pem")

def encrypt_file_hybrid(filename):
    # 1. Generate a random symmetric key
    session_key = Fernet.generate_key()
    f = Fernet(session_key)

    # 2. Encrypt the file data
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)

    # 3. Encrypt the session_key using the RSA Public Key
    with open("public.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())

    encrypted_session_key = public_key.encrypt(
        session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 4. Save the encrypted key and the encrypted file
    with open(filename + ".enc", "wb") as f_out:
        f_out.write(encrypted_session_key + b"---SEP---" + encrypted_data)
    
    print(f"File encrypted to {filename}.enc")

def decrypt_file_hybrid(encrypted_filename):
    # 1. Load the Private Key
    with open("private.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)

    # 2. Split the file to get the encrypted session key and the data
    with open(encrypted_filename, "rb") as f_in:
        content = f_in.read()
        enc_session_key, enc_data = content.split(b"---SEP---")

    # 3. Decrypt the session key using RSA Private Key
    session_key = private_key.decrypt(
        enc_session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 4. Decrypt the data using the session key
    f = Fernet(session_key)
    decrypted_data = f.decrypt(enc_data)

    # 5. Save the decrypted file
    output_name = encrypted_filename.replace(".enc", "_decrypted.txt")
    with open(output_name, "wb") as f_out:
        f_out.write(decrypted_data)
    
    print(f"File decrypted to {output_name}")


# Step 1: Generate the RSA Key Pair
generate_keys()

# Step 2: Create a dummy file to test
with open("homework.txt", "w") as f:
    f.write("This is my secret scripting assignment!")

# Step 3: Encrypt it
encrypt_file_hybrid("homework.txt")

# Step 4: Decrypt it
decrypt_file_hybrid("homework.txt.enc")