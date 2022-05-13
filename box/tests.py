import jwt
import requests as requests
from django.test import TestCase

# Create your tests here.
requests = requests


def login(requests):
    g = requests.post
    print(g)

    def outer(func):
        def inner(w):
            return func(w)
        return inner
    return outer
@login(requests)
def df(w):
    print(w)
    return w


# print(df("eee"))
# url = "http://127.0.0.1:8000/box_mode"
# headers = {
#     "Content-Type": "application/json"
# }
# playload = {
#     "is_log": "sdffffodxx324mkfjigo"
# }
# res = requests.post(url, headers=headers)
# cok = res.cookies.get("is_log")
# print(cok)
import time
import hashlib
import json
import base64


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


# if __name__ == "__main__":
#     # h = json.dumps({"alg":"HS256", "typ": "JWT"})
#     # p = json.dumps(
#     #     {
#     #         "exp": time.time() + 30,
#     #         "iss": "Issuer",
#     #         "iat": time.time(),
#     #         "data": {
#     #             "username": "xjj",
#     #         }
#     #     }
#     # )
#     # k = b"123456"
#     # j = JwtDemo(header=h, paylod=p, key=k)
#     p = {
#             "exp": time.time() + 30,
#             "iss": "Issuer",
#             "iat": time.time(),
#             "data": {
#                 "username": "xjj",
#             }
#         }
#
#     token = jwt.encode(p, "123456", algorithm="HS256")
#     # j = JwtDemo(header=h, paylod=p, key=k)
#     # token = j.jwt_res()
#     print(token)
#     token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTI0MTczMzcuNDg3MzQ3MSwiaXNzIjoiSXNzdWVyIiwiaWF0IjoxNjUyNDE3MzA3LjQ4NzM0NzEsImRhdGEiOnsidXNlcm5hbWUiOiJ4amoifX0.0nzFeIsU4w-bTCt2eJFy441Q5pWG1EjeQoaTZB_NnZw"
#     jwt_deceode = jwt.decode(token, "123456", issuer="Issuer", algorithms=["HS256"])
#     print(jwt_deceode)
