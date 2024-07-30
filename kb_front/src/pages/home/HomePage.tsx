import styled from "styled-components";
import notice from "assets/home/notice.png";
import services from "assets/home/services.png";
import finitems from "assets/home/finitems.png";
import securities from "assets/home/securities.png";
import apps from "assets/home/apps.png";
import footer from "assets/home/footer.png";

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
  width: 50px;
  height: 50px;
  background-color: #f8f8f8;
  border: 1px solid #e5e5e5;
  border-radius: 10px;
  font-size: 40px;
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
  return (
    <HomePageContainer>
      <ChatBotButtonContainer>
        <ChatBotButton>🤖</ChatBotButton>
        <Tooltip>궁금한 용어를 물어보세요!</Tooltip>
      </ChatBotButtonContainer>
      <HomeImage src={notice} />
      <HomeImage src={services} />
      <HomeImage src={finitems} />
      <HomeImage src={securities} />
      <HomeImage src={apps} />
      <HomeImage src={footer} />
    </HomePageContainer>
  );
}
