from fastapi import APIRouter, Request
from utils.authUtil import *
from db.elasticsearchClient import *

router = APIRouter()


@router.get("")
def getChatRooms(request: Request):
    memberId = getMemberIdFromAccessToken(request)
    chatRooms = findChatRoomsByMemberId(memberId)
    return chatRooms


@router.post("")
def createChatRoom(request: Request):
    member = getMemberFromAccessToken(request)
    chatRoomId = esClient.index(index="chatrooms", body={
        "membersId": [member[0]["_id"]],
        "createdAt": datetime.now()
    })["_id"]
    return {"chatRoomId": chatRoomId}
