import jwt
import hashlib
import time, os, base64
from .sql import sql
from .config import config
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random

class file:
    def new(self, file_id, file_enc_b64, or_hash):
        file_enc = base64.b64decode(file_enc_b64)
        nw_hash = hashlib.sha512(file_enc).hexdigest()
        if nw_hash != or_hash:
            return [False, "Error during authenticity check", 400]
        key_2 = Random.new().read(16)
        key_3 = Random.new().read(16)
        key = key_2 + key_3
        file_enc_all = AES.new(key).encrypt(self.__to16(file_enc))
        key_2_b64 = base64.b64encode(key_2).decode('utf-8')
        key3_enc_b64 = base64.b64encode(config().getrsa()["rsa_p1"].encrypt(key_3, 32)[0]).decode('utf-8')
        succes = sql.input("INSERT INTO `file` (id, `key_2`, `hash`) VALUES (%s, %s, %s)", \
        (file_id, key_2_b64, or_hash))
        if not succes:
            return [False, "data input error", 500]
        f = open(f"/home/ged/{file_id}.aes.b64", "w")
        file = base64.b64encode(file_enc_all).decode('utf-8')
        f.write(file)
        f.close()
        return [True, {"key_3": key3_enc_b64}, None]

    def get(self, file_id, hash, key_3):
        res = sql.get("SELECT key_2 FROM file WHERE file.id = %s AND file.hash = %s", (file_id, hash))
        if len(res) < 1:
            return [False, "Invalid id | hash association", 404]
        key = base64.b64decode(res[0][0]) + base64.b64decode(key_3)
        file_enc_b64 = ""
        with open(f"/home/ged/{file_id}.aes.b64", "r") as f:
            tmp = f.read(1)
            while tmp:
                file_enc_b64 += tmp
                tmp = f.read(2048)
        file_enc = base64.b64decode(file_enc_b64)
        file = AES.new(key).decrypt(file_enc)
        nw_hash = hashlib.sha512(file).hexdigest()
        if nw_hash != hash:
            return [False, "Error during authenticity check", 400]
        key_tmp = Random.new().read(32)
        keytmp_enc_b64 = base64.b64encode(config().getrsa()["rsa_p1"].encrypt(key_tmp, 32)[0]).decode('utf-8')
        file_enc = AES.new(key_tmp).encrypt(self.__to16(file))
        file_enc_b64 = base64.b64encode(file_enc).decode('utf-8')
        return [True, {"key": keytmp_enc_b64, "file": file_enc_b64}]

    def __to16(self, str):
        while len(str) % 16 != 0:
            str += b" "
        return str
