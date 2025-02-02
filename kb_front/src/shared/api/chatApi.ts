export const getChatRooms = async () => {
  const accessToken = localStorage.getItem("accessToken");
  if (!accessToken) {
    return [];
  }

  const response = await fetch("http://localhost:8000/chats", {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })
    .then((res) => {
      return res.json();
    })
    .catch((err) => {
      return null;
    });

  if (!response) {
    return [];
  }

  const chatRooms = response.map((chatRoom) => {
    return {
      id: chatRoom["_id"],
      createdAt: chatRoom["_source"]["createdAt"],
    };
  });

  return chatRooms;
};

export const createChatRoom = async () => {
  const accessToken = localStorage.getItem("accessToken");
  if (!accessToken) {
    return null;
  }

  return await fetch("http://localhost:8000/chats", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })
    .then((res) => {
      return res.json();
    })
    .catch((err) => {
      return null;
    });
};

export const getChatsByChatRoomId = async (chatRoomId: string) => {
  const accessToken = localStorage.getItem("accessToken");
  if (!accessToken) {
    return null;
  }

  return await fetch(`http://localhost:8000/chats/${chatRoomId}`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })
    .then((res) => {
      return res.json();
    })
    .catch((err) => {
      return null;
    });
};

export const sendChat = async (chatRoomId: string, content: string) => {
  const accessToken = localStorage.getItem("accessToken");
  if (!accessToken) {
    return null;
  }

  return await fetch(`http://localhost:8000/chats/send`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      chatRoomId,
      content,
    }),
  })
    .then((res) => {
      return res.json();
    })
    .catch((err) => {
      return null;
    });
};

export const sendNoAuthChat = async (content: string) => {
  return await fetch(`http://localhost:8000/chats/send-noAuth`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      content,
    }),
  })
    .then((res) => {
      return res.json();
    })
    .catch((err) => {
      return null;
    });
};
