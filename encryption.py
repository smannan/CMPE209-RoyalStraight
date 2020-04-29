from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


def generateKeys():
    # Generate public key and private key
    prikey = RSA.generate(2048)  # prikey.exportKey() <-- export the key
    pubkey = prikey.publickey()
    return prikey, pubkey


def generateSessionKey():
    return get_random_bytes(16)


def rsa_encrypt(session_key, pubkey):
    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(pubkey)
    enc_session_key = cipher_rsa.encrypt(session_key)
    return enc_session_key


def rsa_decrypt(enc_session_key, prikey):
    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(prikey)
    session_key = cipher_rsa.decrypt(enc_session_key)
    return session_key


#### test ####

# prikey, pubkey = generateKeys()
# session_key = generateSessionKey()
# enc_session_key = rsa_encrypt(session_key, pubkey)
# dec_session_key = rsa_decrypt(enc_session_key, prikey)

# print("Original session_key: ", session_key, "\n Encrypt session key: ",
#       enc_session_key, "\n Dncrypt session key: ", dec_session_key)
