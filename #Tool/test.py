import hashlib
import time, os, base64, requests, json, uuid
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
import socket
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}\n")

test = True

settings = {
"address": "http://172.17.0.1:8080/",
"email": "eliot.courtel@gmail.com",
"password": "test",
"encrypted_password": None,
"file_to_send": "/home/api/test",
"private_key": """-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----"""
}
def main():
    start = time.time()
    f = filevault(settings["address"], settings["email"], settings["password"], settings["encrypted_password"], settings["private_key"])
    version = f.version()
    print(f"Filevault version: {str(version)}")
    init = f.is_init()
    print(f"Filevault initialized: {str(init)}")
    if init is False:
        print("Initializing ...")
        f.init()
    connect = f.connect()
    print(f"Filevault connection: {str(connect)}")
    print(f"Filevault Password: {f.enc}")
    if test is True:
        print(f"\nSecured Exchange: {str(f.test())}")
        data = f.send_file(settings["file_to_send"])
        file = f.get_file(data["id"], data["int_hash"], data["key_1"], data["key_3"])
    done = time.time()
    elapsed = done - start
    print(f"\nDone in {str(round(elapsed, 2))}s")

class filevault:
    def __init__(self,
                 address,
                 email = None,
                 password = None,
                 encrypt_password = None,
                 private_key = None):
        self.api = address
        self.enc = encrypt_password
        self.email = email
        self.password = password
        self.rsa_1 = private_key
        self.rsa_2 = None
        if (encrypt_password is None or private_key is None) and (email is None or password is None):
            raise BaseException("Invalid settings: either encrypt_password and private_key or email and password should be set")
        if self.rsa_1 is not None:
            self.rsa_1 = RSA.importKey(self.rsa_1)

    def version(self):
        response = requests.request("GET", self.api)
        response = json.loads(response.text.encode('utf8'))
        if response["error"] is not None:
            raise BaseException(str(response["status"]) + ": " + str(response["error"]))
        if "Filevault" not in response["data"]:
            raise BaseException("Invalid instance")
        return response["data"]["Filevault"]

    def is_init(self):
        response = requests.request("GET", self.api+"init")
        response = json.loads(response.text.encode('utf8'))
        if response["error"] is not None:
            raise BaseException(str(response["status"]) + ": " + str(response["error"]))
        if "initialized" not in response["data"]:
            raise BaseException("Invalid instance")
        return response["data"]["initialized"]

    def init(self,
             email = None,
             password = None,
             verbose = True):
        email = self.email if email is None else email
        password = self.password if password is None else password
        if email is None or password is None:
            raise BaseException("Should configure email and password if instance isn't initialized")
        if self.rsa_1 is None:
            self.rsa_1 = RSA.generate(4096)
        headers = {'Content-Type': 'application/json'}
        payload = {"email": email, "password": password, "rsa_public": self.rsa_1.publickey().exportKey('PEM').decode('utf-8') }
        response = requests.request("POST", self.api + "init", headers=headers, data = json.dumps(payload))
        response = json.loads(response.text.encode('utf8'))
        if response["error"] is not None:
            raise BaseException(str(response["status"]) + ": " + str(response["error"]))
        password_encrypted = response["data"]["pass"]
        public_encrypted = response["data"]["rsa_p2"]
        byte_tuple = (base64.b64decode(password_encrypted), )
        aes_key_decrypt = self.rsa_1.decrypt(byte_tuple).decode('utf-8')
        aes_key = AES.new(aes_key_decrypt)
        public_encrypted = base64.b64decode(public_encrypted)
        public_decrypted = aes_key.decrypt(public_encrypted).decode('utf-8').strip()
        if verbose is True:
            print(f"\nYour private key: \n{self.rsa_1.exportKey('PEM').decode('utf-8')}\n")
            print(f"Encrypted password: {aes_key_decrypt}\n")
            print(f"Filevault public key's: \n{public_decrypted}\n")
        self.enc = aes_key_decrypt
        return {"your_k": self.rsa_1.exportKey('PEM').decode('utf-8'), "enc_password": aes_key_decrypt, "firevault_p": public_decrypted}

    def connect(self):
        if self.rsa_1 is None:
            raise BaseException("Private key should be set to connect")
        if self.enc is None:
            payload = {"email": self.email, "password": self.password}
        else:
            payload = {"password": self.enc}
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", self.api, headers=headers, data = json.dumps(payload))
        response = json.loads(response.text.encode('utf8'))
        if response["error"] is not None:
            raise BaseException(str(response["status"]) + ": " + str(response["error"]))
        try:
            password_encrypted = response["data"]["pass"]
            public_encrypted = response["data"]["rsa_p2"]
            byte_tuple = (base64.b64decode(password_encrypted), )
            aes_key_decrypt = self.rsa_1.decrypt(byte_tuple).decode('utf-8')
            aes_key = AES.new(aes_key_decrypt)
            public_encrypted = base64.b64decode(public_encrypted)
            public_decrypted = aes_key.decrypt(public_encrypted).decode('utf-8').strip()
            self.rsa_2 = RSA.importKey(public_decrypted)
        except:
            raise BaseException("Invalid Private key")
        self.enc = aes_key_decrypt
        return True

    def send_file(self, path, id=None, key=None, verbose = True):
        file = b""
        with open(path, "rb") as f:
            byte = f.read(1)
            while byte:
                file += byte
                byte = f.read(2048)
        key = Random.new().read(32)
        aes = AES.new(key)
        file_enc = aes.encrypt(self.__to16(file))

        file_enc_b64 = base64.b64encode(file_enc).decode('utf-8')
        hash = hashlib.sha512(file_enc).hexdigest()
        id = str(uuid.uuid4())

        data = {
                'id': id,
                'hash': hash,
                'file_enc_b64': file_enc_b64
               }

        payload = self.prepare(data)
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", self.api + "file", headers=headers, data = json.dumps(payload))
        response = json.loads(response.text.encode('utf8'))
        if response["error"] is not None:
            raise BaseException(str(response["status"]) + ": " + str(response["error"]))
        byte_tuple = (base64.b64decode(response["data"]["key_3"]), )
        key_1 = base64.b64encode(key).decode('utf-8')
        key_3 = base64.b64encode(self.rsa_1.decrypt(byte_tuple)).decode('utf-8')
        if verbose is True:
            print(f"\nPost {id}")
            print(f"  Key_1_b64      : {key_1}")
            print(f"  Key_3_b64      : {key_3}")
            print(f"  Integrity hash : {hash}")
        return {"id": id, "int_hash": hash, "key_1": key_1, "key_3": key_3}

    def get_file(self, id, hash, key_1, key_3, verbose = True):
        data = {
                'id': id,
                'hash': hash,
                'key_3': key_3
               }
        payload = self.prepare(data)
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", self.api + "file/content", headers=headers, data = json.dumps(payload))
        response = json.loads(response.text.encode('utf8'))
        if response["error"] is not None:
            raise BaseException(str(response["status"]) + ": " + str(response["error"]))
        byte_tuple = (base64.b64decode(response["data"]["key"]), )
        key = self.rsa_1.decrypt(byte_tuple)
        file_enc = base64.b64decode(response["data"]["file"])
        file = AES.new(key).decrypt(self.__to16(file_enc))
        res = AES.new(base64.b64decode(key_1)).decrypt(self.__to16(file)).strip()
        nw_hash = hashlib.sha512(file).hexdigest()

        if verbose is True:
            print(f"\nGet  {id}")
            print(f"  Integrity hash original: {hash}")
            print(f"  Integrity hash returned: {nw_hash}")
            print(f"  Integrity check:         {nw_hash == hash}")
        if nw_hash != hash:
            raise BaseException("Integrity check Failed")
        return res

    def test(self):
        data = "test"
        payload = self.prepare(data)
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", self.api + "test/unencode", headers=headers, data = json.dumps(payload))
        response = json.loads(response.text.encode('utf8'))
        if response["error"] is not None:
            raise BaseException(str(response["status"]) + ": " + str(response["error"]))
        return response["data"] == data

    def prepare(self, data):
        key_tmp = Random.new().read(16)
        aes_tmp = AES.new(key_tmp)
        key_tmp_enc_b64 = base64.b64encode(self.rsa_2.encrypt(key_tmp, 32)[0]).decode('utf-8')
        data_enc = aes_tmp.encrypt(self.__to16(json.dumps(data).encode('utf-8')))
        data_enc_b64 = base64.b64encode(data_enc).decode('utf-8')
        return {"key": key_tmp_enc_b64, "data": data_enc_b64}


    def __to16(self, str):
        while len(str) % 16 != 0:
            str += b" "
        return str

if __name__ == "__main__":
    main()
