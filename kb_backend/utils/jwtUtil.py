import jwt
import datetime
from db.redisClient import redisClient

secretKey = "2uaI22VtQR3GLebHv6q52MrH3VLcocXd"


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
        storedAccessToken = redisClient.get(memberEmail)

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