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

export default function ChatContents() {
  const { selectedRoomId } = useSelectedRoomStore();
  const { chats } = useChatsStore();
  const [chatElements, setChatElements] = useState([]);

  useEffect(() => {
    console.log(chats);
    setChatElements(
      chats.map((chat, index) => (
        <ChatScreenContentDiv key={chat.id} $isUser={!chat.isAiResponse}>
          <ChatScreenContent $isUser={!chat.isAiResponse}>
            {index === chats.length - 1 && isNotYetRenderedChat(chat.id) ? (
              <Typical steps={[chat.content]} wrapper="p" />
            ) : (
              chat.content
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
