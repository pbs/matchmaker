import uuid

# Stores the auth_code->device_id relationship
class AuthStorage(object):
	def __init__(self):
		pass

	# Returns the JSON containing the new auth_code
	def dummy_device(self, device_id):
		auth = self.generate_auth(device_id)
		return { "device_id": device_id, "auth_code": auth }

	# Generates a unique auth_code
	def generate_auth(self, device_id):
		auth_code = (uuid.uuid4()).hex[:6]
		while self.get_value(auth_code):
			auth_code = (uuid.uuid4()).hex[:6]
		timeout = { "timeout": 60 * 15 }
		self.add_value(auth_code, device_id, **timeout)
		return auth_code

	# Gets a device based on the auth code provided
	def get_device(self, auth_code, **kwargs):
		return self.get_value(auth_code, **kwargs)

	# Clears the auth->device relationship, so that the code can be used again.
	def remove_auth(self, auth_code):
		return self.del_value(auth_code)

	def get_value(self, key, **kwargs):
		pass

	def add_value(self, key, value, **kwargs):
		pass

	def del_value(self, key, **kwargs):
		pass

