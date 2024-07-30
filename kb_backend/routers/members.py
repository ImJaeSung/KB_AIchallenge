from fastapi import APIRouter
from dto.memberDto import *

router = APIRouter()


@router.post("/login")
def read_root(loginRequest: LoginRequest):
    return {"code": loginRequest.code}
