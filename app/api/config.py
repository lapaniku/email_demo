from string import Template

DEFAULT_ELASTIC_URL = "http://52.166.135.32:9200"

USER_INDEX_TEMPLATE = "w2g_user_{}_deu"
TEAM_INDEX_TEMPLATE = "w2g_team_{}_deu"
GLOBAL_INDEX_TEMPLATE = "w2g_global_deu"
QUERY_TEMPLATE=Template('''
{
  "_source": {
    "exclude": [
      "bodyPart"
    ]
  },
  "from": 0,
  "size": 20,
  "highlight": {
    "fields": {
      "bodyPart": {
        "fragment_size": 300,
        "number_of_fragments": 1
      }
    }
  },
  "query": {
    "bool": {
      "must": {
        "multi_match": {
          "query": "${query}",
          "type": "most_fields",
          "minimum_should_match": "25%",
          "fields": [
            "bodyPart^10"
          ]
        }
      },
      "should": {
        "match": {
          "bodyPart": "${context}"
        }
      }
    }
  }
}
''')