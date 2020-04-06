from elasticsearch_dsl.query import Q, MultiMatch, SF
from .documents import AccountDocument

from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['127.0.0.1'])

def get_search_query(phrase):
    return AccountDocument.search().query("match", holder=phrase)

def search(phrase):
    return get_search_query(phrase).to_queryset()
