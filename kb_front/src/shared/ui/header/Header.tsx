import styled from "styled-components";
import logo from "assets/header/logo.png";
import glasses from "assets/header/glasses.png";
import border from "assets/header/border.png";
import vertical from "assets/header/vertical.png";
import banner from "assets/header/banner.png";
import link from "assets/header/link.png";
import centermenus from "assets/header/centermenus.png";
import { Link, Outlet } from "react-router-dom";
import { useMemberStore } from "shared/store";

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

const LoginContainer = styled.div`
  display: flex;

  width: 980px;
  height: 29px;

  padding: 0 40px;
`;

const LoginDiv = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;

  border: 1px solid #e5e5e5;
  background-color: #fff;
  font-size: 14px;
  width: 64px;

  cursor: pointer;
  z-index: 1;

  &:hover {
    background-color: #f7f7f7;
  }
`;

const Banner = styled.img`
  margin-top: -60px;
`;

const StorylandBox = styled.img`
  margin-top: -200px;

  position: absolute;
  right: 17%;
`;

const CenterMenus = styled.img`
  margin-top: -70px;
  margin-left: -20px;
`;

export default function Header() {
  const { member, isLoading } = useMemberStore();
  const googleClientId =
    "481511611619-a24vhh7i2lcibgvm7dtp9efiukm3bdbl.apps.googleusercontent.com";
  const url = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${googleClientId}&redirect_uri=http://localhost:5173/callback&response_type=code&scope=openid%20profile%20email`;

  return (
    <>
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
          <LoginContainer
            style={{
              display: isLoading ? "none" : member ? "none" : "flex",
            }}
          >
            <LoginDiv>
              <Link
                to={url}
                style={{
                  textDecoration: "none",
                  color: "black",
                }}
              >
                로그인
              </Link>
            </LoginDiv>
            <LoginDiv>인증센터</LoginDiv>
          </LoginContainer>
          <Banner src={banner} />
          <StorylandBox src={link} />
          <CenterMenus src={centermenus} />
        </HeaderInnerDiv>
      </HeaderContainer>
      <Outlet />
    </>
  );
}
