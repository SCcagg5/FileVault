from Model.basic import check, auth
from Object.config import config
from Object.file import file
import json

def version(cn, nextc):
    err = [True, {"Filevault": 1.0}, None]
    return cn.call_next(nextc, err)

def infos(cn, nextc):
    err = config().infos()
    return cn.call_next(nextc, err)

def unencode(cn, nextc):
    err = check.contain(cn.pr, ["key", "data"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.pr = err[1]
    err = config().unencode(cn.pr["key"], cn.pr["data"])
    if err[0]:
        cn.private = err[1]
    return cn.call_next(nextc, err)

def init(cn, nextc):
    err = check.contain(cn.pr, ["email", "password", "rsa_public"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.pr = err[1]
    err = config().init_func(cn.pr["email"], cn.pr["password"], cn.pr["rsa_public"])
    return cn.call_next(nextc, err)

def check_init(cn, nextc):
    err = config().check_init()
    return cn.call_next(nextc, err)

def infos(cn, nextc):
    err = config().infos()
    return cn.call_next(nextc, err)

def get_public(cn, nextc):
    err = check.contain(cn.pr, ["password"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.pr = err[1]
    cn.pr = check.setnoneopt(cn.pr, ["email"])
    err = config().get_public(cn.pr["password"], cn.pr["email"])
    return cn.call_next(nextc, err)

def generate_rsa(cn, nextc):
    size = cn.rt["rsa"] if "rsa" in cn.rt else -1
    err = config().generate_rsa(size)
    return cn.call_next(nextc, err)

def new_file(cn, nextc):
    err = check.contain(cn.private, ["id", "file_enc_b64", "hash"], "BODY.data")
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.pr = err[1]
    cn.pr = check.setnoneopt(cn.pr, ["email"])
    err = file().new(cn.private["id"], cn.private["file_enc_b64"], cn.private["hash"])
    return cn.call_next(nextc, err)

def get_file(cn, nextc):
    err = check.contain(cn.private, ["id","hash", "key_3"], "BODY.data")
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.pr = err[1]
    cn.pr = check.setnoneopt(cn.pr, ["email"])
    err = file().get(cn.private["id"], cn.private["hash"], cn.private["key_3"])
    return cn.call_next(nextc, err)
