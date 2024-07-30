from fastapi import APIRouter
import requests
from dto.memberDto import *

router = APIRouter()


@router.post("/login")
def read_root(loginRequest: LoginRequest):
    accessToken = getGoogleAccessToken(loginRequest.code)
    userEmail = getGoogleUserEmail(accessToken)

    return {"code": loginRequest.code}


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


def getGoogleUserEmail(accessToken):
    getUserInfoUrl = "https://www.googleapis.com/oauth2/v3/userinfo"
    getUserInfoResponse = requests.get(getUserInfoUrl, headers={
        "Authorization": f"Bearer {accessToken}"
    })

    return getUserInfoResponse.json()["email"]
