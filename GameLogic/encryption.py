from Crypto.PublicKey import RSA

from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
import binascii



def generateKeys():
    # Generate public key and private key
    prikey = RSA.generate(2048)
    pubkey = prikey.publickey()
    return prikey.exportKey(), pubkey.exportKey()

def generateSessionKey():
    return get_random_bytes(16)


def rsa_encrypt(session_key, pubkey):
    # Encrypt the session key with the public RSA key
    pubkey = RSA.importKey(pubkey)
    cipher_rsa = PKCS1_OAEP.new(pubkey)
    enc_session_key = cipher_rsa.encrypt(session_key)
    return binary_to_ASCII(enc_session_key)



def rsa_decrypt(enc_session_key, prikey):
    # Decrypt the session key with the private RSA key
    enc_session_key = ASCII_to_binary(enc_session_key)
    prikey = RSA.importKey(prikey)
    cipher_rsa = PKCS1_OAEP.new(prikey)
    session_key = cipher_rsa.decrypt(enc_session_key)
    return binary_to_ASCII(session_key)


def ASCII_to_binary(s):
    return binascii.a2b_base64(s)


def binary_to_ASCII(v):
    return binascii.b2a_base64(v).decode('utf8')

#### test ####

# prikey, pubkey = generateKeys()
# print(pubkey)
# session_key = generateSessionKey()
# encoded_enc_session_key = rsa_encrypt(session_key, pubkey)
# print("encoded session key: ", encoded_enc_session_key)
# dec_session_key = rsa_decrypt(encoded_enc_session_key, prikey)

# print("Original session_key: ", session_key,
#       "\n compare Decrypt session key: ", ASCII_to_binary(dec_session_key))



