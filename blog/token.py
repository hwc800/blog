import time
import hashlib
import json
import base64
import jwt


def get_token(user_id, iss="wchhuang"):
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


def check_token_and(token, issuer="wchhuang") -> dict:
    """token解码"""
    result = {}
    try:
        jwt_deceode = jwt.decode(token, "123456", issuer=issuer, algorithms=["HS256"])
    except:
        return {}
    result["user_id"] = jwt_deceode["data"]["userid"]
    return result


