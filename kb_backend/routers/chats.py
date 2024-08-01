from fastapi import APIRouter, Request
from utils.authUtil import *
from db.elasticsearchClient import *
from datetime import datetime
from dto.chatDto import *

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


@router.get("/{chatRoomId}")
def getChatRoom(request: Request, chatRoomId: str):
    getMemberIdFromAccessToken(request)
    chats = findChatsByChatRoomId(chatRoomId)
    return chats


@router.post("/send")
def createChat(request: Request, sendChatRequest: SendChatRequest):
    getMemberIdFromAccessToken(request)
    userSendTime = datetime.now()
    userChatId = esClient.index(index="chats", body={
        "chatRoomId": sendChatRequest.chatRoomId,
        "isAiResponse": False,
        "content": sendChatRequest.content,
        "createdAt": userSendTime
    })["_id"]

    # TODO: ai 답변 생성하는 로직 추가
    aiResponse = "AI Response"
    aiResponseTime = datetime.now()
    aiChatId = esClient.index(index="chats", body={
        "chatRoomId": sendChatRequest.chatRoomId,
        "isAiResponse": True,
        "content": aiResponse,
        "createdAt": aiResponseTime
    })["_id"]

    return {
        "userChat": {
            "id": userChatId,
            "content": sendChatRequest.content,
            "isAiResponse": False,
            "createdAt": userSendTime
        },
        "aiChat": {
            "id": aiChatId,
            "content": aiResponse,
            "isAiResponse": True,
            "createdAt": aiResponseTime
        }
    }