import styled from "styled-components";
import chatbot from "assets/home/chatbot.png";
import send from "assets/home/send.png";
import { useState } from "react";

const ChatScreenContainer = styled.div`
  position: fixed;
  right: 0;
  bottom: 0;
  width: 400px;
  height: 500px;
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
  height: 427px;
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
  padding: 10px;
  max-width: 70%;
`;

const ChatScreenContentInputContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;

  width: 100%;
  height: 40px;
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
  width: 360px;
  height: 100%;
  padding: 0 10px;
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

  width: 40px;
  height: 100%;
  background-color: #fff;
  border: none;

  &:hover {
    background-color: #e0dbdb;
  }
`;

export default function ChatScreen({ isChatScreenOpen, setIsChatScreenOpen }) {
  return (
    <>
      {isChatScreenOpen ? (
        <ChatScreenContainer>
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
          <ChatScreenContentContainer>
            <ChatScreenContentDiv $isUser={true}>
              <ChatScreenContent $isUser={true}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={false}>
              <ChatScreenContent $isUser={false}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={true}>
              <ChatScreenContent $isUser={true}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={false}>
              <ChatScreenContent $isUser={false}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={true}>
              <ChatScreenContent $isUser={true}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={false}>
              <ChatScreenContent $isUser={false}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={true}>
              <ChatScreenContent $isUser={true}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={false}>
              <ChatScreenContent $isUser={false}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={true}>
              <ChatScreenContent $isUser={true}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={false}>
              <ChatScreenContent $isUser={false}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={true}>
              <ChatScreenContent $isUser={true}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={false}>
              <ChatScreenContent $isUser={false}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={true}>
              <ChatScreenContent $isUser={true}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={false}>
              <ChatScreenContent $isUser={false}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={true}>
              <ChatScreenContent $isUser={true}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={false}>
              <ChatScreenContent $isUser={false}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={true}>
              <ChatScreenContent $isUser={true}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={false}>
              <ChatScreenContent $isUser={false}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={true}>
              <ChatScreenContent $isUser={true}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={false}>
              <ChatScreenContent $isUser={false}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={true}>
              <ChatScreenContent $isUser={true}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
            <ChatScreenContentDiv $isUser={false}>
              <ChatScreenContent $isUser={false}>안녕하세요</ChatScreenContent>
            </ChatScreenContentDiv>
          </ChatScreenContentContainer>
          <ChatScreenContentInputContainer>
            <ChatScreenContentInput placeholder="금융의 뜻이 뭐야?" />
            <ChatScreenInputSendButton>
              <img src={send} />
            </ChatScreenInputSendButton>
          </ChatScreenContentInputContainer>
        </ChatScreenContainer>
      ) : null}
    </>
  );
}
