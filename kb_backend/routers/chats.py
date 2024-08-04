from fastapi import APIRouter, Request
from kb_backend.utils.authUtil import *
from kb_backend.db.elasticsearchClient import *
from datetime import datetime
from kb_backend.dto.chatDto import *
from test import getAiAnswer

router = APIRouter()


@router.get("")
def getChatRooms(request: Request):
    memberId = getMemberIdFromAccessToken(request)
    chatRooms = findChatRoomsByMemberId(memberId)
    return chatRooms


@router.post("")
def createChatRoom(request: Request):
    memberId = getMemberIdFromAccessToken(request)
    createTime = datetime.now()
    chatRoomId = esClient.index(index="chatrooms", body={
        "memberId": memberId,
        "createdAt": createTime
    })["_id"].encode("utf-8")
    return {
        "chatRoomId": chatRoomId,
        "createdAt": createTime
    }


@router.get("/{chatRoomId}")
def getChatRoom(request: Request, chatRoomId: str):
    getMemberIdFromAccessToken(request)
    chats = findChatsByChatRoomId(chatRoomId)
    return chats


@router.post("/send")
def createChat(request: Request, sendChatRequest: SendChatRequest):
    question = sendChatRequest.content
    getMemberIdFromAccessToken(request)
    userSendTime = datetime.now()
    userChatId = esClient.index(index="chats", body={
        "chatRoomId": sendChatRequest.chatRoomId,
        "isAiResponse": False,
        "content": question,
        "createdAt": userSendTime
    })["_id"].encode("utf-8")

    # TODO: ai 답변 생성하는 로직 추가
    df = esIndexToDf("word_dictionary")
    aiResponse = getAiAnswer(df, question)
    aiResponseTime = datetime.now()
    aiChatId = esClient.index(index="chats", body={
        "chatRoomId": sendChatRequest.chatRoomId,
        "isAiResponse": True,
        "content": aiResponse,
        "createdAt": aiResponseTime
    })["_id"].encode("utf-8")
    findNewDataAndSave()

    esClient.indices.refresh(index="chats")
    return {
        "userChat": {
            "id": userChatId,
            "content": question,
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


@router.post("/send-noAuth")
def createChatNoAuth(sendChatRequest: SendNoAuthChatRequest):
    question = sendChatRequest.content
    df = esIndexToDf("word_dictionary")
    aiResponse = getAiAnswer(df, question)
    findNewDataAndSave()

    esClient.indices.refresh(index="chats")
    return {
        "content": aiResponse,
        "isAiResponse": True,
        "createdAt": datetime.now()
    }
