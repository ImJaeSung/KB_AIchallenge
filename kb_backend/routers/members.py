from fastapi import APIRouter, Request
import requests
from dto.memberDto import *
from utils.jwtUtil import *
from db.elasticsearchClient import *
from datetime import datetime

router = APIRouter()


@router.get("/")
def getMemberInfo(request: Request):
    accessToken = request.headers["Authorization"].split(" ")[1]
    memberEmail = getMemberEmailFromAccessToken(accessToken)
    memberData = findMemberByEmail(memberEmail)

    return memberData


@router.post("/login")
def login(loginRequest: LoginRequest):
    accessToken = getGoogleAccessToken(loginRequest.code)
    memberEmail = getGoogleMemberEmail(accessToken)

    accessToken = createAccessToken(memberEmail)
    esClient.index(index="members", body={
        "email": memberEmail,
        "createdAt": datetime.now()
    })
    return {"accessToken": accessToken}


def getGoogleAccessToken(code):
    getGoogleAccessTokenUrl = "https://oauth2.googleapis.com/token"
    getTokenResponse = requests.post(getGoogleAccessTokenUrl, data={
        "client_id": "481511611619-a24vhh7i2lcibgvm7dtp9efiukm3bdbl.apps.googleusercontent.com",
        "client_secret": "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",
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:5173/callback"
    })

    return getTokenResponse.json()["access_token"]


def getGoogleMemberEmail(accessToken):
    getMemberInfoUrl = "https://www.googleapis.com/oauth2/v3/userinfo"
    getMemberInfoResponse = requests.get(getMemberInfoUrl, headers={
        "Authorization": f"Bearer {accessToken}"
    })

    return getMemberInfoResponse.json()["email"]
