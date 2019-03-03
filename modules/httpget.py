from cores.mbrowser import startBrowser
from utils.utils import printf, die

# https://stackoverflow.com/a/4089075

def submit(options, loginInfo, creds, result):
	tryPassword, tryUsername = creds
	realm = loginInfo[0]
	for cred in list(result.queue):
		if tryUsername == cred[0]:
			return True # don't run if find password of username
			
	if options.verbose:
		printf("[+] Trying: %s:%s" %(tryUsername, tryPassword), 'norm')
	
	try:
		proc = startBrowser(options.timeout)
		proc.add_password(options.url, tryUsername, tryPassword, realm)
		proc.open(options.url)
		try:
			proc.open(options.url)
			# printf("[*] Page title: ['%s']" %(proc.title()), "good")
			printf("[*] %s [%s]" %([tryUsername, tryPassword], proc.title()), "good")
			result.put([options.url, tryUsername, tryPassword])
			# printf("[*] Match found: %s" %([tryUsername, tryPassword]), "good") 
		except Exception as err:
			try:
				if err.code == 401:
					if options.verbose:
						printf("[-] Failed %s" %(creds[::-1]), "bad")
				else:
					printf("[x] %s: %s" %(err, creds[::-1]), "bad")
			except:
				die("[x] HTTP GET:", err)
	except:
		if options.verbose:
			printf("[x] Failed!", "bad")