
from Crypto.PublicKey import RSA

key = RSA.generate(2048)
private_key = key.exportKey()
file_out = open("junlan66_private.pem", "wb")
file_out.write(private_key)
file_out.close()

public_key = key.publickey().exportKey()
file_out = open("junlan66_public.pem", "wb")
file_out.write(public_key)
file_out.close()
