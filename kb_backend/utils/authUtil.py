from fastapi import Request
import jwt
import datetime
from kb_backend.db.redisClient import redisClient
from kb_backend.db.elasticsearchClient import *

secretKey = "2uaI22VtQR3GLebHv6q52MrH3VLcocXd"


def getMemberIdFromAccessToken(request: Request):
    accessToken = request.headers["Authorization"].split(" ")[1]
    if not validateAccessToken(accessToken):
        return {"message": "Invalid Access Token"}
    memberEmail = getMemberEmailFromAccessToken(accessToken)
    member = findMemberByEmail(memberEmail)
    if len(member) == 0 or member is None or len(member) > 1:
        raise Exception("Invalid Member")
    return member[0]["_id"]


def createAccessToken(memberEmail):
    expiringTime = datetime.datetime.now() + datetime.timedelta(days=1)
    payload = {
        "memberEmail": memberEmail,
        "exp": expiringTime
    }

    accessToken = jwt.encode(payload, secretKey, algorithm="HS256")

    redisClient.set(memberEmail, accessToken)
    return accessToken


def getMemberEmailFromAccessToken(accessToken):
    if validateAccessToken(accessToken):
        payload = jwt.decode(accessToken, secretKey, algorithms=["HS256"])
        return payload["memberEmail"]


def validateAccessToken(accessToken):
    try:
        payload = jwt.decode(accessToken, secretKey, algorithms=["HS256"])
        memberEmail = payload["memberEmail"]
        storedAccessToken = redisClient.get(memberEmail).decode("utf-8")

        if storedAccessToken is None:
            return False

        return accessToken == storedAccessToken
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False


def deleteAccessToken(accessToken):
    try:
        payload = jwt.decode(accessToken, secretKey, algorithms=["HS256"])
        memberEmail = payload["memberEmail"]
        redisClient.delete(memberEmail)
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
