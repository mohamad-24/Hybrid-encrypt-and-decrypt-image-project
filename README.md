# HybridEncryption
This Python script combines [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) and [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) encryption methods into one to provide a fast and secure hybrid encryption algorithm. It shows how two users would securely transfer files between eachother with an almost zero chance of their message being decrypted by an intercepting attacker.

# Implementation/Scenario
A user wants to receive files from a sender in a secure way:
1. User creates an RSA key pair (publicKey.pem, privateKey.pem)
2. User sends their RSA public key to the sender
3. Sender generates a single-use AES key
4. Sender encrypts all images with the AES key and [Cipher Block Chaining](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_block_chaining_(CBC):~:text=citation%20needed%5D-,Cipher%20block%20chaining%20(CBC),-%5Bedit%5D) mode
5. Sender encrypts the AES key with the provided RSA public key
6. User is sent the encrpyted images and AES key
7. User decrypts the AES key with their RSA private key
8. User decrypts all images with the AES key
9. User deletes the AES single-use key
 
# Installation
1. Install [Python](https://www.python.org/)
2. Install [PyCryptodome](https://pypi.org/project/pycryptodome/)
3. Unzip repository contents and navigate your terminal to this folder
4. Run command: python HybridED.py
5. Test execution can be found in report.pdf
