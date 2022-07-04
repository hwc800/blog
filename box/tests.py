import json
import time

import jwt
import requests as requests
import hashlib
import base64

# Create your tests here.


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
        jwt_res = base64_util(self.header) + b"." + base64_util(self.paylod) + b"." + base64_util(self.sign())
        return jwt_res


# if __name__ == "__main__":
#     h = json.dumps({"alg": "HS256", "typ": "JWT"})
#     p = json.dumps(
#         {
#             "exp": time.time() + 3000,
#             "iss": "Issuer",
#             "iat": time.time(),
#             "data": {
#                 "username": "xjj",
#             }
#         }
#     )
#     k = b"123456"
#     j = JwtDemo(header=h, paylod=p, key=k)
#     token = j.jwt_res()
#     print(token)
#     st = base64.decodebytes(token)
#     print(st)
#     # token = base64.decodebytes(token).decode("utf-8")
#     h, p, f = token.split(b".")
#     print(base64.b64decode(p).decode("utf-8"))


