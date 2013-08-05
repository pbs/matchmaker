import re
from account_base import AccountStorage
from auth_base import AuthStorage

class Matchmaker(object):
	def __init__(self, auth_storage=None, acct_storage=None):
		self.auth = auth_storage
		self.acct = acct_storage

	def get_user(self, device_id):
		"""
		Gets the user id associated with a specific device. It checks
		accounts storage to see if the device_id belongs to any of
		its users. On failure, it returns error message.  On success, it
		returns the user id and device UID.
		"""
		valid = re.match('^[\w_\-=]+$', device_id)
		if not valid:
			return {"error": "Illegal device ID."}

		in_account = self.acct.get_user_of_device(device_id)
		if in_account:
			return {"user_id": in_account, "device_id": device_id}
		else:
			return {"error": "No user exists."}

	def get_auth_code(self, device_id):
		"""
		First step for a device to register itself into Matchmaker.  This
		method registers the device id and returns a auth code
		"""
		# todo: sanitize device_id.  Allow alphanumeric and dash (slug like)
		# return false otherwise
		valid = re.match('^[\w_\-=]+$', device_id)
		if not valid:
			return {"error": "Illegal device ID."}

		return self.auth.dummy_device(device_id) #dummy device dict

	def link_device(self, auth_code, user_id):
		"""
		Associate a device to a user ID. If the attempt to add fails, 
		the additions are reverted.
		"""
		valid = re.match('^[\w_\-=]+$', user_id)
		if not valid:
			return {"error": "Invalid user ID."}
		device_id = self.auth.get_device(auth_code)
		if not device_id:
			return {"error": "No device associated with that auth code."}
		user_exists = self.acct.does_user_exist(user_id)
		if not user_exists:
			return {"error": "No such user exists."}

		# Do we want to allow a force_link parameter to bypass this check?
		user_taken = self.acct.get_user_of_device(device_id)
		if user_taken:
			return {"error": "Another user has already registered this device."}

		ret = self.acct.add_device(user_id, device_id)
		if not ret:
			self.unlink_device(device_id)
			return {"error": "Registration failed."}

		self.auth.remove_auth(auth_code)
		retval = { "device_id": device_id, "user_id": user_id }
		return retval

	def unlink_device(self, device_id):
		valid = re.match('^[\w_\-=]+$', device_id)
		if not valid:
			return {"error": "Invalid user ID."}
		user_id = self.acct.get_user_of_device(device_id)
		if not user_id:
			return {"error": "No user belongs to this device."}
		set = self.acct.remove_device(user_id, device_id)
		if not set:
			return {"error": "Could not remove the device from the user's data."}
		else:
			return {"deleted": "Account/device relationship terminated."}
