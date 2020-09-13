from Model.basic import check, auth
from Object.config import config
import json

def infos(cn, nextc):
    err = config().infos()
    return cn.call_next(nextc, err)

def init(cn, nextc):
    err = check.contain(cn.pr, ["email", "password", "rsa_public"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.pr = err[1]
    err = config().init_func(cn.pr["email"], cn.pr["password"], cn.pr["rsa_public"])
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
