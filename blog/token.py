import time
import hashlib
import json
import base64
import jwt


def get_token(user_id, iss="wchhuang"):
    p = {
        "exp": time.time() + 3600,
        "iss": "%s" % iss,
        "iat": time.time(),
        "data": {
            "userid": "%s" % user_id,
        }
    }

    token = jwt.encode(p, "123456", algorithm="HS256")
    return token


def check_token_and(token, issuer="wchhuang") -> dict:
    result = {}
    try:
        jwt_deceode = jwt.decode(token, "123456", issuer=issuer, algorithms=["HS256"])
    except:
        return {}
    result["user_id"] = jwt_deceode["data"]["userid"]
    return result


