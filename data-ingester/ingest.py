from datetime import datetime
from elasticsearch import Elasticsearch
import logging
import hashlib

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
    'email': 'harrypl@gmail.com',
    'article_likes': ['Kibana', 'Planschade Rijksenergieprojecten', 'Maatschappelijk Verantwoord Innoveren', 'Aardgasvrij'],
    'article_views': ['Kibana', 'Planschade Rijksenergieprojecten', 'Maatschappelijk Verantwoord Innoveren', 'Aardgasvrij']
},
{
    'name': 'Lenz',
    'email': 'lenzylitoni@gmail.com',
    'article_likes': ['Planschade Rijksenergieprojecten', 'Banken met groen fonds', 'Aardgasvrij'],
    'article_views': ['Planschade Rijksenergieprojecten', 'Banken met groen fonds', 'Aardgasvrij', 'Kibana']
},
{
    'name': 'Reit',
    'email': 'rbloom@gmail.com',
    'article_likes': ['Carbon capture', 'Bank falliet', 'Duurzame energie industrie', 'Groene energie opwekken'],
    'article_views': ['Carbon capture', 'Bank falliet', 'Duurzame energie industrie', 'Groene energie opwekken']
},
{
    'name': 'Vicky',
    'email': 'vickster@gmail.com',
    'article_likes': [ 'Aardgasvrij', 'Vrije aardgas hoopjes', 'Waarom aardgasvrij'],
    'article_views': ['Met een waterrad duurzame energie in een handomdraai', 'Aardgasvrij', 'Vrije aardgas hoopjes', 'Waarom aardgasvrij']
},
{
    'name': 'Mumsfeld',
    'email': 'mumsy@gmail.com',
    'article_likes': [],
    'article_views': ['Maatschappelijk Verantwoord Innoveren', 'Blackhole looms', 'From the beyond', 'Spacestation on fire', 
    'The 2000 things you can do to...', 'Aardgasvrij']
},
{
    'name': 'yeoman',
    'email': 'y@gmail.com',
    'article_likes': ['Kolenvrij'],
    'article_views': ['Maatschappelijk Verantwoord Innoveren', 'Kolenvrij']
},
{
    'name': 'Johnny',
    'email': 'johhnyt@gmail.com',
    'article_likes': ['Banken met groen fonds', 'Aardgasvrij'],
    'article_views': ['Banken met groen fonds', 'Aardgasvrij']
},
{
    'name': 'Lenny',
    'email': 'lennyb@gmail.com',
    'article_likes': [],
    'article_views': ['Maatschappelijk verantwoord Innoveren','Kolenvrij', 'Aardgasvrij']
},
{
    'name': 'Katy',
    'email': 'katyl@gmail.com',
    'article_likes': ['Banken met groen fonds', 'Kibana'],
    'article_views': ['Banken met groen fonds', 'Kibana','Kolenvrij']
},
{
    'name': 'Bernard',
    'email': 'bobby@gmail.com',
    'article_likes': ['Economic down falls'],
    'article_views': ['ViQtor Davis', 'Kibana','Kolenvrij']
}]


def remove_index(index_name):
    logger.info("Deleting index %s" % index_name)
    res = es.indices.delete(index=index_name, ignore=[400, 404])
    logger.info("Deletion result: %s" % str(res))


def ingest_dummy_users():
    logger.info("Inserting user data")

    for user in users:
        if "email" not in user:
            logger.warning("user did not contain email attribute")
            continue

        if not user["email"]:
            logger.warning("user email attribute is empty")
            continue

        email_hash_obj = hashlib.md5(str(user["email"]).encode())
        email_id_hash = email_hash_obj.hexdigest()

        res = es.index(index="users-meta", doc_type="user-metadata", body=user, id=email_id_hash)
        logger.info("inserted %s data result: %s" % (user["name"], str(res)))

