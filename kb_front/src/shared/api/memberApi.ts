export const getMemberInfo = async () => {
  const accessToken = localStorage.getItem("accessToken");
  if (!accessToken) {
    return null;
  }

  const response = await fetch("http://localhost:8000/members", {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  }).then((res) => {
    return res.json();
  });

  const member = {
    id: response[0]["_id"],
    email: response[0]["_source"]["email"],
  };
  return member;
};
