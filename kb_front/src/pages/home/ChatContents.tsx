import styled from "styled-components";
import { useChatsStore, useSelectedRoomStore } from "shared/store";
import { useEffect, useState } from "react";

interface Chat {
  id: number;
  isAiResponse: boolean;
  content: string;
  createdAt: Date;
}

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

export default function ChatContents() {
  const { selectedRoomId } = useSelectedRoomStore();
  const { chats } = useChatsStore();
  const [chatElements, setChatElements] = useState([]);

  useEffect(() => {
    setChatElements(
      chats.map((chat) => (
        <ChatScreenContentDiv key={chat.id} $isUser={!chat.isAiResponse}>
          <ChatScreenContent $isUser={!chat.isAiResponse}>
            {chat.content}
          </ChatScreenContent>
        </ChatScreenContentDiv>
      )),
    );
  }, [chats]);

  return (
    <ChatScreenContentContainer>{chatElements}</ChatScreenContentContainer>
  );
}
