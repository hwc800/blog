import base64
import json


def base64_util(d):
    s = d.encode()
    bas = base64.b64encode(s)
    return bas


class CreatToken(object):

    def __init__(self, issu="wchhuang", password="123456789"):
        self.issu = issu
        self.password = password

    def _header(self):
        h = {"alg": "HS256", "typ": "JWT"}

        return base64_util(json.dumps(h))

    def _paylod(self):
        import time

        tm = time.time()

        msg = {
            "exp": tm + 10,  # 设置过期时间，此处为10s
            "Issu": "%s" % self.issu,  # 签名者
            "iat": tm,  # token开始计时的时间戳
            "data": {
                "user_id": 1500,  # 这里是加密信息部分，data自定义
            }
        }

        return base64_util(json.dumps(msg))

    def _sing(self):
        import hashlib

        key = self._header() + b"." + self._paylod()
        result = hashlib.sha256(b"{self.password}")  # 密码需要先sha256
        result.update(key)
        return base64_util(result.hexdigest())  # singe部分最后以16进制用base64加密

    def token(self):
        # 为了更好的体现token的组成，特意如此写，主要为以下三部分。
        return self._header() + b"." + self._paylod() + b"." + self._sing()


def token_is_live(token):
    """解码token，判断是否过期"""
    import time

    h, p, f = token.split(b".")
    de_token = base64.b64decode(p).decode("utf-8")
    de_token = json.loads(de_token)

    if time.time() < int(de_token["exp"]):
        return True

    return False


if __name__ == "__main__":
    q = CreatToken().token()
    # print(q)
    # st = base64.decodebytes(q)
    # print(st)
    # # token = base64.decodebytes(token).decode("utf-8")
    # h, p, f = q.split(b".")
    # exp = base64.b64decode(p).decode("utf-8")
    # print(exp)
    print(token_is_live(q))
