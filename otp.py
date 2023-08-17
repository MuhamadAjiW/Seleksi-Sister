import pyotp
import base64
import hashlib

def generate_totp(secret_key):
    base32_secret = base64.b32encode(secret_key.encode('utf-8')).decode('utf-8')

    print(base32_secret)
    
    totp = pyotp.TOTP(base32_secret, digest=hashlib.sha256, interval=30, digits=8)
    return totp.now()

secret_key = "seleksister2313521095"
totp_code = generate_totp(secret_key)
print("TOTP Code:", totp_code)

uid = "13521095"
upass = uid + ":" + totp_code
print(upass)
base64_upass = base64.b64encode(upass.encode('utf-8')).decode('utf-8')
print(base64_upass)