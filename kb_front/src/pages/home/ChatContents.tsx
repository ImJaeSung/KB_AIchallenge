import React from "react";
import styled from "styled-components";
import {
  isNotYetRenderedChat,
  useChatsStore,
  useSelectedRoomStore,
} from "shared/store";
import { useEffect, useState } from "react";
import { TypeAnimation } from "react-type-animation";
import { summarizeAiChat } from "shared/util";

const ChatScreenContentContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 95%;
  overflow-y: auto;
  color: #000;
  padding: 10px;
`;

const ChatScreenContentDiv = styled.div<{
  $isUser: boolean;
}>`
  display: inline-flex;
  justify-content: ${(props) => (props.$isUser ? "flex-end" : "flex-start")};
  margin: 5px 0;
  padding: 5px;
  width: auto;
`;

const ChatScreenContent = styled.div<{
  $backgroundColor: boolean;
}>`
  background-color: ${(props) => props.$backgroundColor};
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  font-size: 20px;
  padding: 10px;
  max-width: 70%;
  white-space: pre-wrap;
`;

const TypingComponent = ({ content }) => {
  return (
    <TypeAnimation
      sequence={[
        content,
        1000, // 1초 지연 시간
      ]}
      speed={50} // 타이핑 속도를 조절합니다. (밀리초 단위)
      wrapper="span"
      repeat={1}
    />
  );
};

export default function ChatContents() {
  const { selectedRoomId } = useSelectedRoomStore();
  const { chats } = useChatsStore();
  const [chatElements, setChatElements] = useState([]);

  const createAiAnswerComponent = (chat) => {
    const summarizedAiChat = summarizeAiChat(chat.content);
    return (
      <>
        <ChatScreenContent $backgroundColor="rgba(238, 238, 174, 0.8)">
          <span>1. 단어 정의</span>
        </ChatScreenContent>
        <ChatScreenContent $backgroundColor="rgba(238, 238, 174, 0.8)">
          <span>{summarizedAiChat.definition}</span>
        </ChatScreenContent>
        <ChatScreenContent $backgroundColor="rgba(238, 238, 174, 0.8)">
          <span>2. 예시 상황</span>
        </ChatScreenContent>
        <ChatScreenContent $backgroundColor="rgba(238, 238, 174, 0.8)">
          <span>{summarizedAiChat.example}</span>
        </ChatScreenContent>
      </>
    );
  };

  useEffect(() => {
    setChatElements(
      chats.map((chat, index) => (
        <ChatScreenContentDiv key={chat.id} $isUser={!chat.isAiResponse}>
          {chat.isAiResponse ? (
            createAiAnswerComponent(chat)
          ) : (
            <ChatScreenContent $backgroundColor="rgba(238, 238, 174, 0.8)">
              <span>{chat.content}</span>
            </ChatScreenContent>
          )}
        </ChatScreenContentDiv>
      )),
    );
  }, [chats]);

  return (
    <ChatScreenContentContainer>{chatElements}</ChatScreenContentContainer>
  );
}
