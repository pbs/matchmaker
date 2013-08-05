import memcache
from auth_base import AuthStorage

class MemcachedStorage(AuthStorage):
	def __init__(self, SERVER, cache=None):
		if cache:
			self.cache = cache
		else:
			self.cache = memcache.Client([SERVER])

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
