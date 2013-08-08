import uuid

# Stores the auth_code->device_id relationship
class AuthStorage(object):
	def __init__(self):
		pass

	def dummy_device(self, device_id):
		"""
		Returns JSON containing the new auth code and
		stories the auth->device relationship.
		"""
		auth = self._generate_auth(device_id)
		return { "device_id": device_id, "auth_code": auth }
	
	def get_device(self, auth_code, **kwargs):
		"""
		Gets the device that the given auth_code points to.
		"""
		return self.get_value(auth_code, **kwargs)

	def remove_auth(self, auth_code):
		"""
		Clears the auth->device relationship from storage,
		so that the given code can be used again.
		"""
		return self.del_value(auth_code)

	def _generate_auth(self, device_id):
		"""
		Generates a unique auth code, making sure it is
		not currently being used by another device.
		"""
		auth_code = (uuid.uuid4()).hex[:6]
		while self.get_value(auth_code):
			auth_code = (uuid.uuid4()).hex[:6]
		timeout = { "timeout": 60 * 15 }
		self.add_value(auth_code, device_id, **timeout)
		return auth_code

	"""
	To subclass AuthStorage, the only methods you need
	to alter are the three below.
	"""

	def get_value(self, key, **kwargs):
		pass

	def add_value(self, key, value, **kwargs):
		pass

	def del_value(self, key, **kwargs):
		pass

