from nose.tools import *
from matchmaker import Matchmaker, DictionaryAccount, DictionaryAuth
import uuid

def test_dict():
	user_ids = ["new_user_id", "test1", "test2", "test3", "test4"]
	devices = []
	
	print "DICTIONARY IMPLEMENTATION"
	auth = DictionaryAuth()
	acct = DictionaryAccount(user_ids)
	mm = Matchmaker(auth, acct)

	print "ADDING, LINKING"
	for id in user_ids:
		device_id = uuid.uuid4().hex
		devices.append(device_id)
		new_auth = mm.get_auth_code(device_id)
		auth_code = new_auth['auth_code']
		reg_status = mm.link_device(auth_code, id)
		user_status = mm.get_user(device_id)

	print vars(acct)
	print devices

	print "DELETING"
	for dev_id in devices:
		gone = mm.unlink_device(dev_id)

	print vars(acct)
