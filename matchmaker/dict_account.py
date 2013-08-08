from account_base import AccountStorage

# Stores the account/device in a local dict
class DictionaryAccount(AccountStorage):
	def __init__(self, users):
		self.acct_dict = {}	
		for u in users:
			self.acct_dict[u] = []

	def add_device(self, user_id, device_id):
		"""Adds the device to the user's profile"""
		self.acct_dict[user_id].append(device_id)
		return True

	def remove_device(self, user_id, device_id):
		"""Removes the device from the user's information"""
		if user_id in self.acct_dict:
			if self.acct_dict[user_id]:
				self.acct_dict[user_id].remove(device_id)
				return True
		else:
			return False

	def get_user_of_device(self, device_id):
		"""Gets the user for the given device_id, if one exists"""
		users = []
		for key in self.acct_dict:
			if device_id in self.acct_dict[key]:
				users.append(key)

		return users

	def does_user_exist(self, user_id):
		"""Checks if the user exists in account storage"""
		if user_id in self.acct_dict:
			return True
		else:
			return False

