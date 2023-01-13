import glob
import os
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt():
    #Read in RSA public key
    publicKey = RSA.import_key(open("publicKey.pem").read())
    rsaCipher = PKCS1_OAEP.new(publicKey)
    
    #Generate a key for AES encryption
    key = get_random_bytes(32)
    
    #Encrypt the AES key with the RSA public key
    encryptedKey = rsaCipher.encrypt(key)
    
    #Store the encrypted AES key
    file = open("encryptedData.bin", "wb")
    file.write(encryptedKey)
    file.close()
    
    #Read in the .jpg files inside the working directory
    filenames = []
    for filename in glob.glob("*.jpg"):
        filenames.append(filename)
    
    #Encrypt each image with the AES key and initial vector (iv)
    iv = bytes("0123456789abcdef", "utf-8")    
    for filename in filenames:
        #Read in image data
        file = open(filename, "rb")
        data = file.read()
        
        #Encrypt the data with the AES key
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        file.close()
        
        #Write the encrypted data back into the image file
        file = open(filename, "wb")
        file.write(ciphertext)
        file.close()
        
        #Use the first 16 characters of the ciphertext as the iv for encoding the next image
        ciphertextString = b64encode(ciphertext).decode("utf-8")
        iv = ciphertextString[-16:].encode("utf-8")
        
        #Notify user of encryption
        print("Encrypted " + filename)
    
def decrypt():
    #Read in the .jpg files inside the working directory
    filenames = []
    for filename in glob.glob("*.jpg"):
        filenames.append(filename)
    
    #Read in encrypted AES key, and RSA private key
    keyFile = open("encryptedData.bin", "rb")
    privateKey = RSA.import_key(open("privateKey.pem").read())
    encryptedData = keyFile.read(privateKey.size_in_bytes())
    
    #Decrypt the AES key with the RSA private key
    rsaCipher = PKCS1_OAEP.new(privateKey)
    key = rsaCipher.decrypt(encryptedData)
    keyFile.close()
    
    #Decrypt each image with the AES key and initial vector (iv)
    iv = bytes("0123456789abcdef", "utf-8")
    for filename in filenames:
        #Read in image data
        file = open(filename, "rb")
        encryptedData = file.read()
        
        #Decrypt the data with the AES key
        ciphertextString = b64encode(encryptedData).decode("utf-8")
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(encryptedData), AES.block_size)
        file.close()
        
        #Write the decrypted data back into the image file
        file = open(filename, "wb")
        file.write(plaintext)
        file.close()
        
        #Use the first 16 characters of the ciphertext as the iv for decoding the next image
        iv = ciphertextString[-16:].encode("utf-8")

        #Notify user of decryption
        print("Decrypted " + filename)
        
    #Delete AES key
    os.remove("encryptedData.bin");

userInput = "0"
while userInput != "3":
    print("Enter '1' to encrypt files")
    print("Enter '2' to decrypt files")
    print("Enter '3' to quit")
    userInput = input("...: ")
    if userInput == "1":
        encrypt()
    if userInput == "2":
        decrypt()
