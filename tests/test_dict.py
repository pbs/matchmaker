from nose.tools import *
from matchmaker.globals import ALLOW_MULTIPLE
from matchmaker import Matchmaker, DictionaryAccount, DictionaryAuth
import uuid, pprint

def test_dict():
	user_ids = ["new_user_id", "test1", "test2", "test3", "test4"]
	devices = []
	
	print "DICTIONARY IMPLEMENTATION"
	auth = DictionaryAuth()
	acct = DictionaryAccount(user_ids)
	mm = Matchmaker(auth, acct, multi=ALLOW_MULTIPLE)

	print "ADDING, LINKING"
	for id in user_ids:
		device_id = uuid.uuid4().hex
		devices.append(device_id)
		new_auth = mm.get_auth_code(device_id)
		auth_code = new_auth['auth_code']
		reg_status = mm.link_device(auth_code, id)
		user_status = mm.get_user(device_id)

	for dev in devices:
		new_auth = mm.get_auth_code(dev)
		reg_status = mm.link_device(new_auth['auth_code'], user_ids[0])
		user_status = mm.get_user(dev)

	print mm.get_user(devices[0])
	print mm.get_user(devices[1])
	print mm.get_user(devices[2])
	pprint.pprint(vars(acct))
	print devices
	
	print "DELETING"
	for dev_id in devices:
		gone = mm.unlink_device(dev_id, user_ids[0])
		print gone

	print vars(acct)
