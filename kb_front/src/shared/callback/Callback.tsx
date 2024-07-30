import React, { useEffect, useState, useRef } from "react";
import { useNavigate, useLocation } from "react-router-dom";

export default function GoogleCallback() {
  const [isProcessing, setIsProcessing] = useState(true);
  const navigate = useNavigate();
  const location = useLocation();
  const processedRef = useRef(false);

  useEffect(() => {
    const processCallback = async () => {
      if (processedRef.current) return;
      processedRef.current = true;

      const urlParams = new URLSearchParams(location.search);
      const code = urlParams.get("code");

      if (code) {
        // 서버로 코드 전송 및 토큰 수신
        const { accessToken, refreshToken } = await fetch(
          `http://localhost:8000/members/login`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              code,
            }),
          },
        ).then((response) => response.json());

        // 토큰을 로컬 스토리지에 저장
        localStorage.setItem("accessToken", accessToken);
        localStorage.setItem("refreshToken", refreshToken);

        // 홈페이지로 리다이렉트
        navigate("/");
      }

      setIsProcessing(false);
    };

    processCallback();
  }, [navigate, location]);

  if (isProcessing) {
    return <div>로그인 처리 중...</div>;
  }

  return null;
}
