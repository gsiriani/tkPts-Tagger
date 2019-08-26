from tkpt_tagger import TkPt_Tagger
from mongotriggers import MongoTrigger
from pymongo import MongoClient
import mongo_setup as mongo_setup

tagger = TkPt_Tagger()

def notify_manager(op_document):
	print(op_document['o'])
	print('\nNew Message:\n' + op_document['o']['text'])
	tag = tagger.Classify(op_document['o']['text'])
	print('\nPredicted tag:\n' + tag)
	result = db.messages.update_one({'_id': op_document['o']['_id']}, {'$set':{'tag': tag}})
	print(result)

mongo_setup.global_init()

client = MongoClient(host='localhost', port=3001)
db = client.meteor

triggers = MongoTrigger(client)
triggers.register_insert_trigger(notify_manager, 'meteor', 'messages')
triggers.tail_oplog()

