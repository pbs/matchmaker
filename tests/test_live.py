from nose.tools import *
from matchmaker import Matchmaker, GigyaStorage, MemcachedStorage
from matchmaker.globals import GIGYA_API_KEY, GIGYA_SECRET, ALLOW_MULTIPLE
import json, requests, uuid, pprint

def test_live():
	filename = "tests/test_users.txt"
	f = open(filename)
	user_ids = []
	for i in range(0, 5):
		user_ids.append(f.readline().strip())
	f.close()
	print user_ids
	devices = []

	print "LIVE IMPLEMENTATION"
	auth = MemcachedStorage("127.0.0.1:11211")
	acct = GigyaStorage(GIGYA_API_KEY, GIGYA_SECRET)
	mm = MatchmakerMulti(auth, acct, multi=ALLOW_MULTIPLE)
	
	print "ADDING, LINKING"
	for id in user_ids:
		print "-------"
		device_id = uuid.uuid4().hex
		devices.append(device_id)
		new_auth = mm.get_auth_code(device_id)
		auth_code = new_auth['auth_code']
		reg_status = mm.link_device(auth_code, id)
		print "Registration", reg_status

	print "Pausing for Gigya to catch up. Press ENTER to continue."
	enter = raw_input() 

	print "TESTING ALLOW_MULTIPLE"
	# NOTE: This works 80% of the time. Considering the device will
	# be polling get_user, this stress-test thing shouldn't be as
	# necessary.
	for dev_id in devices:
		new_auth = mm.get_auth_code(dev_id)
		auth_code = new_auth['auth_code']
		reg_status = mm.link_device(auth_code, user_ids[0])
		print reg_status

	print "Pausing for Gigya to catch up. Press ENTER to continue."
	enter = raw_input() 

	for dev_id in devices:
		user_status = mm.get_user(dev_id)
		pprint.pprint(user_status)

	print "DELETING"
	for dev_id in devices:
		auth_code = new_auth['auth_code']
		reg_status = mm.link_device(auth_code, user_ids[0])
		user_status = mm.get_user(dev_id)
		print user_status
		gone = mm.unlink_device(dev_id)
		print gone

