import styled from "styled-components";
import chatbot from "assets/home/chatbot.png";
import send from "assets/home/send.png";
import ChatContents from "./ChatContents.tsx";
import {
  notYetRendered,
  useChatRoomsStore,
  useChatsStore,
  useMemberStore,
  useSelectedRoomStore,
} from "shared/store";
import { useEffect } from "react";
import {
  createChatRoom,
  getChatsByChatRoomId,
  sendChat,
  sendNoAuthChat,
} from "shared/api";

const ChatScreenOuter = styled.div`
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;

  width: 80vw;
  height: 90vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`;

const ChatScreenInner = styled.div`
  width: 100%;
  height: 95%;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const ChatHistoriesContainer = styled.div`
  width: 20vw;
  height: 100%;
  padding: 3px;
  overflow-y: auto;

  background-color: rgba(238, 238, 174, 0.8);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
`;

const ChatHistoryDiv = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 5px 0;
  padding: 5px;
  height: 40px;
  width: auto;

  font-size: 20px;

  &:hover {
    background-color: #f1e58c;
    cursor: pointer;
  }
`;

const ChatScreenContainer = styled.div`
  width: 60vw;
  height: 100%;
  color: #fff;
  background-color: rgba(255, 255, 255, 0.8);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
`;

const ChatScreenHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 10px;
  border-bottom: 1px solid #e5e5e5;
  color: #000;

  width: 100%;
  height: 5%;

  background-color: rgba(238, 238, 174, 0.8);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
`;

const ChatScreenHeaderButtons = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const ChatScreenCloseButton = styled.button`
  display: flex;
  justify-content: center;
  align-items: center;

  background-color: transparent;
  border: none;
  color: #000;
  font-size: 20px;
  cursor: pointer;
`;

const ChatScreenContentInputContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;

  width: 100%;
  height: 5%;
  border-top: 1px solid #e5e5e5;
  border-left: none;
  border-right: none;
  border-bottom: none;
  outline: none;
  font-size: 16px;

  background-color: rgba(238, 238, 174, 0.8);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
`;

const ChatScreenContentInput = styled.input`
  width: 93%;
  height: 100%;
  padding: 0 10px;
  font-size: 20px;
  border: none;
  background-color: transparent;
  outline: none;

  &::placeholder {
    color: #a78686;
    opacity: 0.5;
  }
`;

const ChatScreenInputSendButton = styled.button`
  display: flex;
  justify-content: center;
  align-items: center;

  width: 7%;
  height: 100%;
  background-color: #fff;
  border: none;

  &:hover {
    background-color: #e0dbdb;
  }
`;

export default function ChatScreen({ isChatScreenOpen, setIsChatScreenOpen }) {
  const { selectedRoomId, setSelectedRoom } = useSelectedRoomStore();
  const { chatRooms, addChatRoom } = useChatRoomsStore();
  const { chats, setChats, addChat } = useChatsStore();
  const { member } = useMemberStore();

  useEffect(() => {
    const handleEsc = (event) => {
      if (event.key === "Escape") {
        setIsChatScreenOpen(false);
        setSelectedRoom(null);
        setChats([]);
      }
    };

    if (isChatScreenOpen) {
      window.addEventListener("keydown", handleEsc);
    } else {
      window.removeEventListener("keydown", handleEsc);
    }

    return () => {
      window.removeEventListener("keydown", handleEsc);
    };
  }, [isChatScreenOpen, setIsChatScreenOpen]);

  useEffect(() => {
    const getChatsAndSet = async () => {
      if (member) {
        const findChats = await getChatsByChatRoomId(selectedRoomId);
        setChats(findChats);
      } else {
        const findChats = JSON.parse(localStorage.getItem(selectedRoomId));
        setChats(findChats);
      }
    };

    if (selectedRoomId) {
      const selectedChatRoom = document.getElementById(selectedRoomId);
      selectedChatRoom.style.backgroundColor = "#f1e58c";
      getChatsAndSet();
    }
  }, [selectedRoomId]);

  const handleSendChat = async () => {
    const inputDoc = document.getElementById("content-input");
    if (!inputDoc.value) {
      return;
    }
    const question = inputDoc.value;
    inputDoc.value = "";

    const chat = {
      id: chats.length + 1,
      isAiResponse: false,
      content: question,
      createdAt: new Date(),
    };

    if (!member) {
      if (selectedRoomId) {
        addChat(chat);

        const aiChatResponse = await sendNoAuthChat(question);
        const aiChat = {
          id: chats.length + 2,
          ...aiChatResponse,
        };
        localStorage.setItem(
          selectedRoomId,
          JSON.stringify([...chats, chat, aiChat]),
        );
        notYetRendered.push(aiChat.id);
        setChats([...chats, chat, aiChat]);
      } else {
        const newChatRoom = {
          id: chatRooms.length + 1,
        };
        addChatRoom(newChatRoom);
        localStorage.setItem(
          "chatRooms",
          JSON.stringify([...chatRooms, newChatRoom]),
        );
        addChat(chat);
        const aiChatResponse = await sendNoAuthChat(question);
        const aiChat = {
          id: chats.length + 2,
          ...aiChatResponse,
        };
        localStorage.setItem(newChatRoom.id, JSON.stringify([chat, aiChat]));
        notYetRendered.push(aiChat.id);

        setSelectedRoom(newChatRoom.id);
      }
    } else {
      if (selectedRoomId) {
        addChat(chat);

        const { userChat, aiChat } = await sendChat(selectedRoomId, question);
        notYetRendered.push(aiChat.id);

        setChats([...chats, userChat, aiChat]);
      } else {
        const { chatRoomId, createdAt } = await createChatRoom();
        addChatRoom({ id: chatRoomId, createdAt });
        addChat(chat);
        const { aiChat } = await sendChat(chatRoomId, question);
        notYetRendered.push(aiChat.id);

        setSelectedRoom(chatRoomId);
      }
    }
  };

  const handleClickChatRoom = (event) => {
    if (selectedRoomId) {
      const pastSelectedChatRoom = document.getElementById(selectedRoomId);
      pastSelectedChatRoom.style.backgroundColor = "transparent";
    }

    const chatRoomId = event.target.id;
    setSelectedRoom(chatRoomId);
  };

  return (
    <>
      {isChatScreenOpen ? (
        <ChatScreenOuter>
          <ChatScreenHeader>
            <img
              src={chatbot}
              style={{
                width: "20px",
                height: "20px",
              }}
            />
            <ChatScreenHeaderButtons>
              <ChatScreenCloseButton
                onClick={() => {
                  setIsChatScreenOpen(false);
                  setSelectedRoom(null);
                  setChats([]);
                }}
              >
                X
              </ChatScreenCloseButton>
            </ChatScreenHeaderButtons>
          </ChatScreenHeader>
          <ChatScreenInner>
            <ChatHistoriesContainer id="chat-histories-container">
              {[...chatRooms].reverse().map((chatRoom, index) => (
                <ChatHistoryDiv
                  id={chatRoom.id}
                  key={chatRoom.id}
                  onClick={handleClickChatRoom}
                >
                  {chatRooms.length - index}번째 대화
                </ChatHistoryDiv>
              ))}
            </ChatHistoriesContainer>
            <ChatScreenContainer>
              <ChatContents />
              <ChatScreenContentInputContainer>
                <ChatScreenContentInput
                  placeholder="금융의 뜻이 뭐야?"
                  id="content-input"
                  autoComplete="off"
                  onKeyPress={(event) => {
                    if (event.key === "Enter") {
                      handleSendChat();
                    }
                  }}
                />
                <ChatScreenInputSendButton onClick={handleSendChat}>
                  <img src={send} />
                </ChatScreenInputSendButton>
              </ChatScreenContentInputContainer>
            </ChatScreenContainer>
          </ChatScreenInner>
        </ChatScreenOuter>
      ) : null}
    </>
  );
}
