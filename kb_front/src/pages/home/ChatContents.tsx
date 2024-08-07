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

const AiChatContentContainer = styled.div`
  display: flex;
  flex-direction: column;
`;

const AiChatTitle = styled.div`
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
`;

const AiChatContent = styled.div`
  font-size: 20px;
  padding: 10px;
  background-color: rgba(238, 238, 174, 0.8);
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
  white-space: pre-wrap;
  max-width: 80%;
`;

const TypingComponent = ({ content, delay }) => {
  return (
    <TypeAnimation
      sequence={[
        content,
        delay, // 지연 시간
      ]}
      speed={80} // 타이핑 속도
      wrapper="span"
      repeat={1}
    />
  );
};

const AiAnswerComponent = ({ chat }) => {
  const summarizedAiChat = summarizeAiChat(chat.content);
  const [showTitle1, setShowTitle1] = useState(false);
  const [showContent1, setShowContent1] = useState(false);
  const [showTitle2, setShowTitle2] = useState(false);
  const [showContent2, setShowContent2] = useState(false);
  const [showTitle3, setShowTitle3] = useState(false);
  const [showContent3, setShowContent3] = useState(false);

  useEffect(() => {
    // 순차적으로 표시되도록 설정
    const timer1 = setTimeout(() => setShowTitle1(true), 0);
    const timer2 = setTimeout(() => setShowContent1(true), 500);
    const timer3 = setTimeout(() => setShowTitle2(true), 5000);
    const timer4 = setTimeout(() => setShowContent2(true), 5500);
    const timer5 = setTimeout(() => setShowTitle3(true), 10000);
    const timer6 = setTimeout(() => setShowContent3(true), 10500);

    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
      clearTimeout(timer3);
      clearTimeout(timer4);
      clearTimeout(timer5);
      clearTimeout(timer6);
    };
  }, []);

  return (
    <AiChatContentContainer>
      {showTitle1 && (
        <AiChatTitle>
          <TypingComponent content="1. 단어 정의" delay={500} />
        </AiChatTitle>
      )}
      {showContent1 && (
        <AiChatContent>
          <TypingComponent content={summarizedAiChat.definition} delay={500} />
        </AiChatContent>
      )}
      {showTitle2 && (
        <AiChatTitle style={{ marginTop: "10px" }}>
          <TypingComponent content="2. 예시 상황" delay={500} />
        </AiChatTitle>
      )}
      {showTitle2 && (
        <AiChatContent>
          <TypingComponent content={summarizedAiChat.example} delay={500} />
        </AiChatContent>
      )}
      {showContent3 && (
        <AiChatTitle>
          <TypingComponent content="3. 상품 추천" delay={500} />
        </AiChatTitle>
      )}
      {showContent3 && (
        <AiChatContent>
          <TypingComponent
            content={summarizedAiChat.recomendation}
            delay={500}
          />
        </AiChatContent>
      )}
    </AiChatContentContainer>
  );
};

export default function ChatContents() {
  const { selectedRoomId } = useSelectedRoomStore();
  const { chats } = useChatsStore();
  const [chatElements, setChatElements] = useState([]);

  useEffect(() => {
    setChatElements(
      chats.map((chat) => (
        <ChatScreenContentDiv key={chat.id} $isUser={!chat.isAiResponse}>
          {chat.isAiResponse ? (
            isNotYetRenderedChat(chat.id) ? (
              <AiAnswerComponent chat={chat} />
            ) : (
              <AiChatContentContainer>
                <AiChatTitle>1. 단어 정의</AiChatTitle>
                <AiChatContent>
                  {summarizeAiChat(chat.content).definition}
                </AiChatContent>
                <AiChatTitle>2. 예시 상황</AiChatTitle>
                <AiChatContent>
                  {summarizeAiChat(chat.content).example}
                </AiChatContent>
                <AiChatTitle>3. 세 번째 제목</AiChatTitle>
                <AiChatContent>
                  {summarizeAiChat(chat.content).recomendation}
                </AiChatContent>
              </AiChatContentContainer>
            )
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
