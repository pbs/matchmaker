import memcache
from auth_base import AuthStorage

class MemcachedStorage(AuthStorage):
	def __init__(self, server, cache=None):
		if not (server or cache):
			raise ValueError("No server set for memcached! Please check your globals.py file and try again.")
		if cache:
			self.cache = cache
		else:
			self.cache = memcache.Client([server])

	def get_value(self, key, **kwargs):
		ret = ""
		try:
			ret = self.cache.get(str(key))
		except:
			raise Exception()
		return ret

	def add_value(self, key, value, **kwargs):
		timeout = ""
		if 'timeout' in kwargs: 
			timeout = kwargs['timeout']
		else:
			timeout = 0

		try:
			self.cache.set(str(key), value, timeout)
		except:
			return {"error": "Key error."}
		ret = self.cache.get(str(key))
		return ret

	def del_value(self, key, **kwargs):
		try:
			self.cache.delete(str(key))
			return True
		except:
			return False
