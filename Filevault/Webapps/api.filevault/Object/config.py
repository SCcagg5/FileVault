import jwt
import hashlib
import time, os, base64
from .sql import sql
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES

class config:
    def __init__(self):
        self.init = False
        res = sql.get("SELECT COUNT(`config`.`id`) FROM config", ())[0][0]
        if res == 1:
            self.init = True

    def check_init(self):
        ret = [False, "System isn't initialized.", 401]
        if self.init is True:
            ret = [True, {}, None]
        return  ret

    def init_func(self, email, password, rsa_p1):
        if self.init is True:
            return [False, "System is already initialized.", 401]
        password = self.__hash(email, password)
        print(password)
        enc = self.__second_encode(password)
        rsa_2 = RSA.generate(4096)
        succes = sql.input("INSERT INTO `config` (id, `password`, `rsa_p1`, `rsa_k2`) VALUES (NULL, %s, %s, %s)", \
        (enc, rsa_p1, rsa_2.exportKey('PEM').decode('utf-8')))
        if not succes:
            return [False, "data input error", 500]
        pass_encrypt = base64.b64encode(RSA.importKey(str.encode(rsa_p1)).encrypt(str.encode(password), 32)[0]).decode('utf-8')
        public_encrypt = AES.new(password)
        public_encrypt = base64.b64encode(public_encrypt.encrypt(self.__to16(rsa_2.publickey().exportKey('PEM').decode('utf-8')))).decode('utf-8')
        return [True, {"pass": pass_encrypt, "rsa_p2": public_encrypt}, None]

    def get_public(self, password, email = None):
        if email is not None:
            enc = self.__second_encode(password)
        else:
            password = self.__hash(email, password)
            enc = self.__second_encode(password)
        res = sql.get("SELECT password, rsa_p1, rsa_k2", ())[0]
        if enc != res[0]:
            return [False, "Invalid credentials", 403]
        rsa_1 = RSA.importKey(str.encode(res[1]))
        rsa_2 = RSA.importKey(str.encode(res[2]))
        pass_encrypt = base64.b64encode(rsa_1.encrypt(str.encode(password), 32)[0]).decode('utf-8')
        public_encrypt = AES.new(password)
        public_encrypt = public_encrypt.encrypt(self.__to16(rsa_2.publickey().exportKey('PEM').decode('utf-8')))
        return [True, {"pass": pass_encrypt, "rsa_p2": public_encrypt}, None]

    def generate_rsa(self, size = 4096):
        """do not use, use a custom rsa key generator"""
        try:
            size = int(size)
        except:
            return [False, "Invalid size " + str(size), 400]
        if size == -1:
            size = 1024
        if size % 256 != 0 or size < 1024:
            return [False, "The key RSA modulus length must be a multiple of 256 and >= 1024", 400]
        key = RSA.generate(size)
        ret = {
                "private": key.exportKey('PEM').decode('utf-8'),
                "public": key.publickey().exportKey('PEM').decode('utf-8'),
                "size": size
               }
        return [True, ret, 200]

    def __getsecret(self):
        return str(os.getenv('API_SCRT', '!@ws4RT4ws212@#%'))

    def __hash(self, email, password):
        if password is None or email is None:
            return None
        s = len(email)
        n = s % (len(password) - 1 if len(password) > 1 else 1)
        secret = self.__getsecret()
        salted = password[:n] + str(s) + password[n:] + secret
        hashed = hashlib.sha256(salted.encode('utf-8')).hexdigest()
        key = hashlib.md5(hashed.encode('utf-8')).hexdigest()
        while len(key) < 32:
            key += key
        return key[:32]

    def __getIV(self):
        scrt = self.__getsecret()
        while len(scrt) < 16:
            scrt += scrt
        return  scrt[:16]

    def __to16(self, str):
        while len(str) % 16 != 0:
            str += " "
        return str

    def __second_encode(self, password):
        return hashlib.sha512(password.encode('utf-8')).hexdigest()
