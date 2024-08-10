export function summarizeAiChat(content) {
  console.log("content: ", content);
  const chats = content.split("\n\n");
  return {
    definition: chats[0].substring("1. 단어 정의\n".length),
    example: chats[1].substring("2. 예시 상황\n".length),
    recomendation: chats[2].substring("3. 상품 추천\n".length),
  };
}
