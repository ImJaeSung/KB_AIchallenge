import styled from "styled-components";
import notice from "assets/home/notice.png";

const HomePageContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

const Notice = styled.img`
  margin-top: 60px;
`;
export default function HomePage() {
  return (
    <HomePageContainer>
      <Notice src={notice} />
    </HomePageContainer>
  );
}
