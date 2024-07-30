from elasticsearch import Elasticsearch, helpers

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