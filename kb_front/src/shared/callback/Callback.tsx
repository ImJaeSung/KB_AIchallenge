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
        const response = await fetch(`http://localhost:8000/members/login`, {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            code,
          }),
        }).then((response) => response.json());

        localStorage.setItem("accessToken", response.accessToken);

        navigate("/");
      }

      setIsProcessing(false);
    };

    processCallback();
  }, [navigate, location]);

  if (isProcessing) {
    return null;
  }

  return null;
}
