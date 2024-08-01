import styled from "styled-components";
import notice from "assets/home/notice.png";
import services from "assets/home/services.png";
import finitems from "assets/home/finitems.png";
import securities from "assets/home/securities.png";
import apps from "assets/home/apps.png";
import footer from "assets/home/footer.png";
import chatbot from "assets/home/chatbot.png";
import { useMemberStore } from "shared/store";
import { useEffect, useState } from "react";
import { getMemberInfo } from "shared/api";
import ChatScreen from "./ChatScreen.tsx";

const HomePageContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

const ChatBotButtonContainer = styled.div`
  position: fixed;
  right: 10%;
  top: 10%;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const ChatBotButton = styled.button`
  display: flex;
  justify-content: center;
  align-items: center;

  width: 50px;
  height: 50px;
  background-color: #f8f8f8;
  border: 1px solid #e5e5e5;
  border-radius: 10px;
  font-size: 50px;
  cursor: pointer;
  position: relative;

  &:hover + span {
    visibility: visible;
    opacity: 1;
  }
`;

const Tooltip = styled.span`
  visibility: hidden;
  opacity: 0;
  width: 120px;
  background-color: #555;
  color: #fff;
  text-align: center;
  border-radius: 5px;
  padding: 5px;
  position: absolute;
  top: 50%;
  left: calc(100% + 10px); /* 위치를 버튼의 오른쪽으로 설정 */
  transform: translateY(-50%);
  transition: opacity 0.3s;

  &::after {
    content: "";
    position: absolute;
    top: 50%;
    right: 100%; /* 삼각형이 왼쪽에 나타나도록 설정 */
    transform: translateY(-50%);
    border-width: 5px;
    border-style: solid;
    border-color: transparent #555 transparent transparent;
  }
`;

const HomeImage = styled.img`
  margin-top: 60px;
`;

export default function HomePage() {
  const [isChatScreenOpen, setIsChatScreenOpen] = useState(false);
  const { setMember, setIsLoading } = useMemberStore();

  useEffect(() => {
    const getMemberInfoAndSet = async () => {
      const memberData = await getMemberInfo();
      if (memberData) {
        setMember(memberData);
      }

      setIsLoading(false);
    };

    if (!localStorage.getItem("accessToken")) {
      setIsLoading(false);
      return;
    }

    getMemberInfoAndSet();
  }, []);

  return (
    <HomePageContainer>
      <ChatBotButtonContainer>
        <ChatBotButton
          onClick={() => {
            setIsChatScreenOpen(!isChatScreenOpen);
          }}
        >
          <img src={chatbot} />
        </ChatBotButton>
        <Tooltip>궁금한 용어를 물어보세요!</Tooltip>
      </ChatBotButtonContainer>
      <HomeImage src={notice} />
      <HomeImage src={services} />
      <HomeImage src={finitems} />
      <HomeImage src={securities} />
      <HomeImage src={apps} />
      <HomeImage src={footer} />
      <ChatScreen
        isChatScreenOpen={isChatScreenOpen}
        setIsChatScreenOpen={setIsChatScreenOpen}
      />
    </HomePageContainer>
  );
}
