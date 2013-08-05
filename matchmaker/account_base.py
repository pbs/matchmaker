# Stores the device data in the user's profile.
class AccountStorage(object):
	def __init__(self):
		pass

	def add_device(self, user_id, device_id):
		"""Adds the device to the user's profile"""
		pass

	def remove_device(self, user_id, device_id):
		"""Removes the device from the user's information"""
		pass

	def get_user_of_device(self, device_id):
		"""Gets the user for the given device_id, if one exists"""
		pass

	def does_user_exist(self, user_id):
		"""Checks if the user exists in account storage"""
		pass

