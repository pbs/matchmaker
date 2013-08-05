from nose.tools import *
from matchmaker import Matchmaker, GigyaStorage, MemcachedStorage
from matchmaker.globals import GIGYA_API_KEY, GIGYA_SECRET
import json, requests, uuid

def test_live():
	filename = "tests/test_users.txt"
	f = open(filename)
	user_ids = f.read().split("\n")
	f.close()
	devices = []

	print "LIVE IMPLEMENTATION"
	auth = MemcachedStorage("127.0.0.1:11211")
	acct = GigyaStorage(GIGYA_API_KEY, GIGYA_SECRET)
	mm = Matchmaker(auth, acct)
	
	print "ADDING, LINKING"
	for id in user_ids:
		device_id = uuid.uuid4().hex
		devices.append(device_id)
		new_auth = mm.get_auth_code(device_id)
		auth_code = new_auth['auth_code']
		reg_status = mm.link_device(auth_code, id)
		print reg_status
		user_status = mm.get_user(device_id)

	print "DELETING"
	for dev_id in devices:
		gone = mm.unlink_device(dev_id)
		print gone

