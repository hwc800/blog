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
            "exp": tm + 10,
            "Issu": "%s" % self.issu,
            "iat": tm,
            "data": {
                "user_id": 1500,
            }
        }

        return base64_util(json.dumps(msg))

    def _sing(self):
        import hashlib

        key = self._header() + b"." + self._paylod()
        result = hashlib.sha256(b"{self.password}")
        result.update(key)
        return base64_util(result.hexdigest())

    def token(self):
        return self._header() + b"." + self._paylod() + b"." + self._sing()


def token_is_live(token):
    import time

    h, p, f = token.split(b".")
    de_token = base64.b64decode(p).decode("utf-8")
    de_token = json.loads(de_token)

    if time.time() < int(de_token["exp"]):
        return True

    return False


# if __name__ == "__main__":
    # q = CreatToken().token()
    # print(q)
    # st = base64.decodebytes(q)
    # print(st)
    # # token = base64.decodebytes(token).decode("utf-8")
    # h, p, f = q.split(b".")
    # exp = base64.b64decode(p).decode("utf-8")
    # print(exp)
    # print(token_is_live(q))
