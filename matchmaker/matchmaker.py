import re
from account_base import AccountStorage
from auth_base import AuthStorage

class Matchmaker(object):
	"""
	The Matchmaker class is the central class of this library. It pulls
	from two unrelated data sources, one meant to store temporary authorization
	codes (auth_storage), the other storing any amount of data about your
	users; Matchmaker will only use a fraction of the data stored in your
	account storage. Using these two sources, Matchmaker handles the 
	device activation process.

	params:
		auth_storage: AuthStorage of where your auth codes will be stored
		acct_storage: AccountStorage where your user profiles are stored
		multi: determines whether or not you want a device to potentially
		have multiple users linked to it. The default value disables this
		behavior.
	"""
	def __init__(self, auth_storage, acct_storage, multi=False):
		self.auth = auth_storage
		self.acct = acct_storage
		self.multi = multi

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
		# in_account will always be a list; if self.multi is false,
		# it will be a list of just one user.
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

		# Sanity check: do both the device and user exist?
		device_id = self.auth.get_device(auth_code)
		if not device_id:
			return {"error": "No device associated with that auth code."}
		user_exists = self.acct.does_user_exist(user_id)
		if not user_exists:
			return {"error": "No such user exists."}

		# From Edgar: Do we want to allow a force_link parameter to bypass this check?
		# If we're allowing multiple users per device, check if the device->user relationship
		# already exists. If not self.multi, just check if some user already has it registered.
		user_taken = self.acct.get_user_of_device(device_id)
		if user_taken and (user_id in user_taken) and self.multi:
			return {"error": "This device is already registered to you!"}
		elif not self.multi and user_taken:
			return {"error": "Another user has already registered this device."}

		# Add the device to the account. If it fails, unlink the device.
		ret = self.acct.add_device(user_id, device_id)
		if not ret:
			self.unlink_device(device_id)
			return {"error": "Registration failed."}

		# And if it succeeds, remove the auth from auth_storage so it can be used again
		self.auth.remove_auth(auth_code)
		retval = { "device_id": device_id, "user_id": user_id }
		return retval

	def unlink_device(self, device_id, user_id=False):
		"""
		Removes a specific device->user relationship. If a device is not allowed to have
		multiple users, the user_id field is optional. If multi is true, the
		user_id parameter is required, as the device could be connected with multiple
		users.
		"""
		# If multiple users per device are allowed, you must provide a user_id
		if not user_id and self.multi:
			return {"error": "Multiple users allowed and no user_id is present!"}

		# If multi is false, it's possible they may not have given you a user_id
		valid = re.match('^[\w_\-=]+$', device_id)
		if not valid:
			return {"error": "Invalid user ID."}
		if not user_id:
			user_id = self.acct.get_user_of_device(device_id)
			if not user_id:
				return {"error": "No user belongs to this device."}

		# Unlink the device!
		set = self.acct.remove_device(user_id, device_id)
		if not set:
			return {"error": "Could not remove the device from the user's data."}
		else:
			return {"deleted": "Account/device relationship terminated."}
