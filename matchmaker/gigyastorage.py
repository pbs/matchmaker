import requests, json
from account_base import AccountStorage

class GigyaStorage(AccountStorage):
	def __init__(self, api_key, secret):
		if not (api_key and secret):
			raise ValueError("Your Gigya access keys are empty. Please check your globals.py file and try again.")
		self.credentials = { "apiKey": api_key, "secret": secret }
		self.set_url = "https://accounts.gigya.com/accounts.setAccountInfo"
		self.get_url = "https://accounts.gigya.com/accounts.search"

	def add_device(self, uid, device_id):
		"""
		Links a user to a device. If the attempt fails, the function
		returns false.
		"""
		return self._set_device(uid, device_id)

	def get_user_of_device(self, device_id):
		"""
		Get the user (or users, if multiple users is allowed) for
		a given device. Returns a list of 1+ users.
		"""
		query = "SELECT UID FROM accounts WHERE data.devices.id_s = '%s'" % (device_id)
		params = { "query": query }
		uid = self._query(params, "get")
		if uid['results']:
			return [id['UID'] for id in uid['results']]
		else:
			return False

	def does_user_exist(self, uid):
		"""
		Checks to see if the given user_id exists in Gigya.
		"""
		query = "SELECT UID FROM accounts WHERE UID='%s'" % (uid,)
		params = {"query": query}
		uid = self._query(params, "get")
		if uid['results']:
			return uid['results'][0]
		else:
			return False

	def remove_device(self, uid, device_id):
		return self._set_device(uid, device_id, remove=True)

	def _get_device(self, uid, device_id=None):
		"""
		Returns False on a status error, the list of devices if it exists,
		a specific device if requested, or a blank devices dict if no devices exist.
		"""

		query = "SELECT data.devices FROM accounts WHERE UID='%s'" % uid
		params = { "query": query }
		devices = self._query(params, "get")

		if 'statusCode' in devices and devices['statusCode'] == 403:
			return False
		elif 'results' in devices and devices['results']:
			devices = devices['results'][0]['data']
			return devices
		else:
			devices = { "devices": [ ] }
			return devices

	def _set_device(self, uid, device_id, remove=False):
		"""
		Either adds or removes a device from the user's list of
		devices in Gigya. Returns False on a status error, and otherwise
		returns the status of the query to alter the device data
		in Gigya.
		"""
		#Get all devices for this user
		devices = self._get_device(uid)
		new_device = { "id_s": device_id, "is_active_b": True }

		#If the user had devices, append; otherwise, write the 'devices'
		#JSON for this user.
		if not devices:
			return False
		elif devices['devices']:
			for d in devices['devices']:
				if d['id_s'] == device_id:
					if remove:
						devices['devices'].remove(d)
					else: #found the device when we're trying to register it
						return False
			if not remove:
				devices['devices'].append(new_device)
		else:
			devices['devices'].append(new_device)

		params = { "UID": uid}
		params.update(data = json.dumps(devices))
		retval = self._query(params, "set")
		return retval

	def _query(self, p, type):
		url = self.set_url if type is "set" else self.get_url
		params = dict(self.credentials)
		if p:
			params.update(p)
		if "set":
			r = requests.post(url=url, data=params, verify=False)
		else:
			r = requests.get(url=url, params=params, verify=False)
		return json.loads(r.text)
