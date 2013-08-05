matchmaker
======

Matchmaker is an authentication library for PBS, meant to connect a user's
Over-The-Top (OTT) devices such as the AppleTV, Roku, and GoogleTV to
the user's MyPBS video content stored in his/her PBS Gigya account. The
service can be accessed either as a library or a web API. Both methods
have a two-part authentication flow.

sample code
-------------
The following sample code is test code meant to automatically run through the entire registration flow. In production, this is actually a two-step process; part 1 occurs only on the device, while part 2 is a call made from the user's browser.

	from matchmaker import Matchmaker, GigyaStorage, MemcachedStorage
	
	auth = MemcachedStorage("127.0.0.1:11211")
	acct = GigyaStorage("the_api_key", "the_secret")
	mm = Matchmaker(auth_storage=auth, acct_storage=acct)

	device_id = "test_device"
	uid = "_guid_lAtpDqR_emDPQB5dcb6iLVP-eBkAC32J2ySHwUsFGjs="
	
	# Part 1: Device doesn't have a user.
	auth_code = mm.get_auth_code(device_id)
	
	# Part 2: Try to register the user.
	added = mm.register_user(auth_code['auth_code'], uid)

	# Part 3: There is a user registered for the device, and 'result' will have its UID.
	user_id = mm.get_user(device_id)

authentication flow
-------------
As displayed above, registering a device is a two-part process. 

#### Part 1: From the device
In your app, call get_auth_code() if the user attempts to access content where registration is required. Display a "register your device?" page on the device containing this auth code. From this page, continuously poll get_user() to see if the user has completed registration.

#### Part 2: On the browser
Create a small registration page where the user can enter his/her account name and authorization code. Keep this registration process short, since the user has a limited time to enter the code before it expires. Calling register_user() sends this data to Matchmaker, which will return the registration success/failure.


storage information
-------------

This service is primarily one of data integration. For the authentication flow, there are up to three possible storage locations:
* Authentication storage: stores the auth code->device relationship. Since auth keys should be short, they should also expire after a time period.
* Account storage: stores any number of things about a given user, most of which is specific to your application and unimportant to this service. Among the rest of a user's information, this service will store a list of all the devices he/she has registered. Matchmaker is type-agnostic; a user can have as many devices of any type as your storage mechanism can reasonably hold.

access functions
-------------

### get_auth_code()
* Parameters: device_id
* Use: Call to generate a time_sensitive authorization code to link this device to a user. 
* Diagram: <a href="https://s3.amazonaws.com/uploads.hipchat.com/24330/346822/6ovza43nc4hvjaa/Matchmaker.get_auth_code().png">link</a>

Returns the following json:

	{
		"device_id": "the device id sent in the call",
		"auth_code": "3ub893"
	}

Possible `error_message` returns:
* Illegal device ID: the device_id you sent contains characters other than alphanumerics or _-=

### link_device()
* Parameters: auth_code, user_id
* Use: Call to associate a user with a device, based on the auth_code given in the call. This will add the device->user relationship in account storage. If the registration process is successful, Matchmaker will automatically remove the auth code.
* Diagram: <a href="https://s3.amazonaws.com/uploads.hipchat.com/24330/346822/n4w7tf29ex0lf2a/Matchmaker.link_device()%20(2).png">link</a>
 
Resulting JSON:

	{
		"device_id": "the device id sent in the call",
		"user_id": "_guid_etc=="
	}
	
Possible `error_message` returns:
* Illegal user ID: the user_id you sent contains characters other than alphanumerics or _-=
* No device associated with that auth code: either the auth code expired, or the user entered the auth code wrong
* No such user exists: Matchmaker checked your user storage and found no user matching that user_id
* Another user has already registered this device: Matchmaker does not currently support having multiple users linked to the same device. Unlink the device, or ponder your failings.
* Registration failed: something went awry in your account storage's add_device method

### get_user()
* Parameters: device_id
* Use: Continuously poll this function to see if device->user assocation has been completed. See the JSON return values below.
* Diagram: <a href="https://s3.amazonaws.com/uploads.hipchat.com/24330/346822/6ovza43nc4hvjaa/Matchmaker.get_auth_code().png">link</a>

Returns the following json:

	{
		"device_id": "the device id sent in the call",
		"user_id": "_guid_etc=="
	}

Possible `error_message` returns:
* Illegal device ID: the device_id you sent contains characters other than alphanumerics or _-=
* No such user exists: Matchmaker checked your user storage and found no user matching that user_id

### unlink_device()
* Parameters: device_id
* Use: Call to remove the device->user relationship from account storage. This will only remove the specific device data - the rest of the account data is left untouched.
* Diagram: <a href="https://s3.amazonaws.com/uploads.hipchat.com/24330/346822/hrmw7tlux801dok/Matchmaker.unlink_device().png">here</a>

Resulting JSON:

	{
		"deleted": "Account/device relationship terminated."
	}

Possible `error_message` returns:
* Illegal user ID: the user_id you sent contains characters other than alphanumerics or _-=
* No user belongs to this device: after checking your account storage, no user was found that had registered the device specified
* Could not remove the device from the user's data: something went awry in your account storage's remove_device() method
