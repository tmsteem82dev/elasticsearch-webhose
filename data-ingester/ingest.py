from datetime import datetime
from elasticsearch import Elasticsearch
import logging

logger = logging.getLogger("uniLogger")
logger.setLevel(logging.DEBUG)

log_fileHandler = logging.FileHandler("ingest.log")
log_fileHandler.setLevel(logging.DEBUG)

# Create console handler with higher log level
log_consoleHandler = logging.StreamHandler()
log_consoleHandler.setLevel(logging.INFO)

log_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_fileHandler.setFormatter(log_formatter)
log_consoleHandler.setFormatter(log_formatter)

logger.addHandler(log_fileHandler)
logger.addHandler(log_consoleHandler)


es = Elasticsearch()

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}

def dummy_data():
    res = es.index(index="test-index", doc_type="tweet", id=1, body=doc)

    logger.info("result: " + str(res['result']))

    res = es.get(index="test-index", doc_type="tweet", id=1)

    logger.info("es.get result: " + str(res["_source"]))

    es.indices.refresh(index="test-index")

    res = es.search(index="test-index", body={"query": {"match_all": {}}})

    logger.info("Got %d hits:" % res["hits"]["total"])

    for hit in res["hits"]["hits"]:
        logger.info("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

users = [{
    'name': 'harry',
    'article_likes': ['Planschade Rijksenergieprojecten', 'Maatschappelijk Verantwoord Innoveren', 'Aardgasvrij']

},
{
    'name': 'Lenz',
    'article_likes': ['Planschade Rijksenergieprojecten', 'Banken met groen fonds', 'Aardgasvrij']
},
{
    'name': 'Reit',
    'article_likes': ['Carbon capture', 'Bank falliet', 'Duurzame energie industrie', 'Groene energie opwekken']
},
{
    'name': 'Vicky',
    'article_likes': ['Met een waterrad duurzame energie in een handomdrai', 'Aardgasvrij', 'Vrije aardgas hoopjes', 'Waarom aardgasvrij']
},
{
    'name': 'Mumsfeld',
    'article_likes': ['Maatschappelijk Verantwoord Innoveren', 'Blackhole looms', 'From the beyond', 'Spacestation on fire', 'The 2000 things you can do to...']
},
{
    'name': 'Mumsfeld',
    'article_likes': ['Blackhole looms']
}]

def remove_index(index_name):
    logger.info("Deleting index %s" % index_name)
    es.indices.delete(index=index_name, ignore=[400, 404])

def ingest_dummy_users():
    logger.info("Inserting user data")

    for user in users:
        res = es.index(index="users-meta", doc_type="user-metadata", body=user)

