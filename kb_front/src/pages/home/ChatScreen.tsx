import styled from "styled-components";
import chatbot from "assets/home/chatbot.png";

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
  border-radius: 10px;
`;

const ChatScreenHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 10px;
  border-bottom: 1px solid #e5e5e5;
  color: #000;
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
        </ChatScreenContainer>
      ) : null}
    </>
  );
}
