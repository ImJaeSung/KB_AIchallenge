from elasticsearch import Elasticsearch, helpers
import pandas as pd
import ast

esClient = Elasticsearch(
    hosts=["http://172.16.147.137:9200"],
    http_auth=("elastic", "wns1254"),
    scheme="http",
    port=9200
)


def saveBulkData(data):
    actions = [
        {
            "_index": "word_dictionary",
            "_type": "_doc",
            "_source": doc
        }
        for doc in data
    ]

    helpers.bulk(esClient, actions)


def findMemberByEmail(email):
    searchResult = esClient.search(
        index="members",
        body={
            "query": {
                "match": {
                    "email": email
                }
            }
        }
    )

    return searchResult["hits"]["hits"]


def findChatRoomsByMemberId(memberId):
    try:
        searchResult = esClient.search(
            index="chatrooms",
            body={
                "query": {
                    "match": {
                        "memberId": memberId
                    }
                }
            }
        )

        return searchResult["hits"]["hits"]
    except Exception as e:
        print(f"Error: {str(e)}")
        return []


def findChatsByChatRoomId(chatRoomId):
    try:
        searchResult = esClient.search(
            index="chats",
            body={
                "query": {
                    "match": {
                        "chatRoomId": chatRoomId
                    }
                }
            }
        )

        result = []

        for item in searchResult["hits"]["hits"]:
            source = item["_source"]
            chat_data = {
                "id": item["_id"],
                "isAiResponse": source["isAiResponse"],
                "content": source["content"],
                "createdAt": source["createdAt"]
            }
            result.append(chat_data)

        return result
    except Exception as e:
        print(f"Error: {str(e)}")
        return []

def esIndexToDf(index):
    df = esClient.search(index=index, body={"query": {"match_all": {}}})["hits"]["hits"]
    for i in range(len(df)):
        df[i]["_source"]["embedding"] = ast.literal_eval(df[i]["_source"]["embedding"])
        df[i] = df[i]["_source"]

    df = pd.DataFrame(df)
    return df

