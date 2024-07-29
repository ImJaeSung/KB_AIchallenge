import styled from "styled-components";

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

  background-color: #cf4242;
`;

export default function Header() {
  return (
    <HeaderContainer>
      <HeaderInnerDiv>
        <HeaderMenuContainer />
        <h1>Header</h1>
      </HeaderInnerDiv>
    </HeaderContainer>
  );
}
