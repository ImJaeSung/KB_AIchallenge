import styled from "styled-components";
import chatbot from "assets/home/chatbot.png";
import send from "assets/home/send.png";
import { useState } from "react";
import { useChatRoomsStore } from "../../shared/store";

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
  }
`;

const ChatScreenContainer = styled.div`
  width: 60vw;
  height: 100%;
  background-color: #000;
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

const ChatScreenContentContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 95%;
  overflow-y: auto;
  color: #000;
  padding: 10px; /* 컨테이너의 패딩 추가 */
`;

const ChatScreenContentDiv = styled.div<{
  $isUser: boolean;
}>`
  display: inline-flex; /* inline-flex로 설정하여 너비가 콘텐츠에 맞게 조정되도록 함 */
  justify-content: ${(props) => (props.$isUser ? "flex-end" : "flex-start")};
  margin: 5px 0;
  padding: 5px;
  width: auto;
`;

const ChatScreenContent = styled.p<{
  $isUser: boolean;
}>`
  background-color: ${(props) =>
    props.$isUser ? "rgba(238, 238, 174, 0.8)" : "#f9f0b4"};
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  font-size: 20px;
  padding: 10px;
  max-width: 70%;
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
  const { chatRooms } = useChatRoomsStore();

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
                }}
              >
                X
              </ChatScreenCloseButton>
            </ChatScreenHeaderButtons>
          </ChatScreenHeader>
          <ChatScreenInner>
            <ChatHistoriesContainer>
              {[...chatRooms].reverse().map((chatRoom, index) => (
                <ChatHistoryDiv key={chatRoom.id}>
                  {chatRooms.length - index}번째 대화
                </ChatHistoryDiv>
              ))}
            </ChatHistoriesContainer>
            <ChatScreenContainer>
              <ChatScreenContentContainer></ChatScreenContentContainer>
              <ChatScreenContentInputContainer>
                <ChatScreenContentInput placeholder="금융의 뜻이 뭐야?" />
                <ChatScreenInputSendButton>
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
