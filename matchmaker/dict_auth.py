import uuid
from auth_base import AuthStorage
from datetime import datetime, timedelta

# Stores the auth_code->device_id relationship in a local dict
class DictionaryAuth(AuthStorage):
	def __init__(self):
		self.auth_dict = {}

	def get_value(self, key, **kwargs):
		if key not in self.auth_dict:
			return False
		time_gap = (datetime.now() - self.auth_dict[key]["time"]).seconds 
		if time_gap >= 60 * 15:
			del self.auth_dict[key]
			return False
		else:
			return self.auth_dict[key]["value"]

	def add_value(self, key, value, **kwargs):
		timeout = datetime.now()

		self.auth_dict[key] = {"time": timeout, "value": value}
		return self.auth_dict[key]

	def del_value(self, key, **kwargs):
		del self.auth_dict[key]

