from fastapi import APIRouter, Request
from utils.authUtil import *
from db.elasticsearchClient import *
from datetime import datetime

router = APIRouter()


@router.get("")
def getChatRooms(request: Request):
    memberId = getMemberIdFromAccessToken(request)
    chatRooms = findChatRoomsByMemberId(memberId)
    return chatRooms


@router.post("")
def createChatRoom(request: Request):
    memberId = getMemberIdFromAccessToken(request)
    chatRoomId = esClient.index(index="chatrooms", body={
        "memberId": memberId,
        "createdAt": datetime.now()
    })["_id"]
    return {"chatRoomId": chatRoomId}
