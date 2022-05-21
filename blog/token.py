import time
import hashlib
import json
import base64
import jwt


def get_token(user_id, iss="sos425300"):
    p = {
        "exp": time.time() + 3600,  # token过期时间
        "iss": "%s" % iss,  # token鉴权者
        "iat": time.time(),  # token开始计算的时间撮
        "data": {
            "userid": "%s" % user_id,  # 加密信息，可自定义
        }
    }

    token = jwt.encode(p, "123456", algorithm="HS256")
    return token


def check_token_and(token, issuer="sos425300") -> dict:
    """token解码"""
    result = {}
    try:
        jwt_deceode = jwt.decode(token, "123456", issuer=issuer, algorithms=["HS256"])
    except:
        return {}
    result["user_id"] = jwt_deceode["data"]["userid"]
    return result


def base64_util(d):
    s = d.encode()
    b_s = base64.b64encode(s)
    return b_s


def hmac_util(key, s):
    m = hashlib.sha256(key)
    m.update(s)
    return m.hexdigest()


class JwtDemo:
    def __init__(self, header, paylod, key):
        self.header = header
        self.paylod = paylod
        self.key = key

    def sign(self):
        bs_header = base64_util(self.header)
        bs_payload = base64_util(self.paylod)
        s_group = bs_header + b"." + bs_payload
        return hmac_util(self.key, s_group)

    def jwt_res(self):
        jwt_res = base64_util(self.header) + b"." + base64_util(self.paylod) + b"." +base64_util(self.sign())
        return jwt_res

#
# if __name__ == "__main__":
    token = get_token(user_id=100)
    print(token)
    h, p, f = token.split(".")
    print(p)
    g = base64.b64decode(p)
    print(g)

