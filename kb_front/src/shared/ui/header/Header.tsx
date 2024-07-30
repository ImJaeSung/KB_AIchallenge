import styled from "styled-components";
import logo from "assets/logo.png";
import glasses from "assets/glasses.png";
import border from "assets/border.png";
import vertical from "assets/vertical.png";

const HeaderContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;

  width: 100%;
  height: 530px;

  background-color: #effce6;
`;

const HeaderInnerDiv = styled.div`
  display: block;
  justify-content: center;

  padding: 3px;
  width: 980px;
  height: 100%;
`;

const HeaderMenuContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;

  width: 100%;
  height: 32px;
  margin: 0 12px;
`;

const HeaderMenus = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 640px;
  height: 32px;

  font-size: 14px;
  font-weight: 400;
`;

export default function Header() {
  return (
    <HeaderContainer>
      <HeaderInnerDiv>
        <HeaderMenuContainer>
          <img src={logo} />
          <HeaderMenus>
            개인 기업 <img src={vertical} style={{ margin: "0 8px" }} />
            자산관리 부동산 퇴직연금 카드{" "}
            <img src={vertical} style={{ margin: "0 5px" }} /> 전체 서비스{" "}
            <img src={border} style={{ margin: "0 5px" }} />{" "}
            <img src={vertical} style={{ margin: "0 5px" }} /> Global{" "}
            <img src={border} style={{ margin: "0 5px" }} />
            <img src={glasses} />
          </HeaderMenus>
        </HeaderMenuContainer>
      </HeaderInnerDiv>
    </HeaderContainer>
  );
}
