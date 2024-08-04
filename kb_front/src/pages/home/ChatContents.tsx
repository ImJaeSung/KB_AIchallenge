import React from "react";
import styled from "styled-components";
import {
  isNotYetRenderedChat,
  useChatsStore,
  useSelectedRoomStore,
} from "shared/store";
import { useEffect, useState } from "react";
import Typical from "react-typical";

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
  $isUser: boolean;
}>`
  background-color: ${(props) =>
    props.$isUser ? "rgba(238, 238, 174, 0.8)" : "#f9f0b4"};
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  font-size: 20px;
  padding: 10px;
  max-width: 70%;
  white-space: pre-wrap;
`;

export default function ChatContents() {
  const { selectedRoomId } = useSelectedRoomStore();
  const { chats } = useChatsStore();
  const [chatElements, setChatElements] = useState([]);

  const processLineBreaks = (content) => {
    return content.split("\n").map((line, index, array) => (
      <React.Fragment key={index}>
        {line}
        {index < array.length - 1 && <br />}
      </React.Fragment>
    ));
  };

  useEffect(() => {
    setChatElements(
      chats.map((chat, index) => (
        <ChatScreenContentDiv key={chat.id} $isUser={!chat.isAiResponse}>
          <ChatScreenContent $isUser={!chat.isAiResponse}>
            {index === chats.length - 1 && isNotYetRenderedChat(chat.id) ? (
              <Typical steps={[chat.content, chat.content]} wrapper="span" />
            ) : (
              processLineBreaks(chat.content)
            )}
          </ChatScreenContent>
        </ChatScreenContentDiv>
      )),
    );
  }, [chats]);

  return (
    <ChatScreenContentContainer>{chatElements}</ChatScreenContentContainer>
  );
}
