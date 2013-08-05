from nose.tools import *
from matchmaker import Matchmaker, GigyaStorage, MemcachedStorage

def test_auth():
	""" Tests the key validation stuff to make sure failing keys really fail """
	acct = GigyaStorage("asejifoa", "agoeuiau")
	auth = MemcachedStorage("127.0.0.1:11211")
	mm = Matchmaker(auth_storage=auth, acct_storage=acct)

	ids = [	
	# Working keys
		"fji39qp", 
		"fji32-", 
		"fjwo-=_", 
		"fjie1245", 
	# Failing keys
		"fjeiw%^&", 
		"!fjies'",
		"$asd",
		"'888'",
		"`qaz"
	]

	for id in ids:
		auth = mm.get_auth_code(id)
		print id, auth
