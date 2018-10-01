import requests
from requests.auth import HTTPBasicAuth
from core import utils

# http://docs.python-requests.org/en/master/user/authentication/
# USING PROXY WITH REQUESTS https://stackoverflow.com/a/13395324
# TODO Using proxy

def submit(URL, tryUsername, tryPassword, proxy, verbose, result):
	if verbose:
		utils.printf("Trying: %s:%s" %(tryUsername, tryPassword), 'norm')
	
	try:

		resp = requests.get(URL, auth = HTTPBasicAuth(tryUsername, tryPassword))
		
		if resp.status_code == 200:
			result.put([tryUsername, tryPassword])
			utils.printf("Match found: %s:%s" %(tryUsername, tryPassword), "good") 
			# pass
		elif resp.status_code == 401:
			if verbose:
				utils.printf("Failed: %s:%s" %(tryUsername, tryPassword), "bad")
		else:
			# unknown
			pass
	except Exception as err:
		utils.die("Runtime error", err)