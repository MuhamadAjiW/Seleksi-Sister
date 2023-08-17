import pyotp
import base64
import hashlib
import requests

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

url = "http://recruit.sister20.tech/submit/b"
data = {'fullName': 'Muhamad Aji Wibisono', 'link': "https://github.com/MuhamadAjiW/SeleksiSister23", "message":"https://www.youtube.com/watch?v=L-aviGyL4c4&ab_channel=brombo"}
headers = {'Content-Type': 'application/json', 'Authorization': 'Basic ' + base64_upass}
response = requests.post(url, json=data, headers=headers)

print("\nstatus code:", response.status_code)
print("Response content:")
print(response.text)
