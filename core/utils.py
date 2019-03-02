import sys

def prints(mtext, spaces = 2):
	#############################################
	#	print message and replace it after
	#	Use for status bar, brute forcing process
	#	https://stackoverflow.com/a/5291044
	#
	#	Update code by this (Works better)
	#	https://stackoverflow.com/a/41511658
	#############################################

	#######
	#	Newer version:
	#	https://stackoverflow.com/a/3173338
	#######

	# Print bar to screen
	# sys.stdout.write("%s%s\n" %("\n" * spaces, mtext))
	# sys.stdout.flush()
	# # Clean line, remove all characters
	# for text in reversed(mtext.split("\n")):
	# 	# Move up cursor 1 line
	# 	sys.stdout.write("\033[F")
	# 	# Clean current line
	# 	sys.stdout.write("%s\r" %(" " * len(text)))
	# sys.stdout.write("\033[F" * spaces)
	
	sys.stdout.write("%s\r" %(mtext))
	sys.stdout.flush()
	sys.stdout.write("%s\r" %(" " * len(mtext)))

def progress_bar(trying, completed, total, bsize = 60):
	"""
		MULTIPLE LINES PROGRESS BAR IS NOT WORKING FOR WINDOWS AND ANDROID TERM
		Create a progress bar to show current process
		Progessbar format [+++#####-----]
			+ is completed tasks. Tasks should recived responses
			# is submited tasks. Tasks have no responses
			- is waiting tasks
	"""
	finished = (completed * bsize) / total
	running = (trying * bsize) / total - finished
	running = 1 if running < 1 else running

	prints("|%s%s%s| %10s" %(
		finished * "+",
		running * "#",
		(bsize - finished - running) * '-',
		completed
	))


def printf(mtext, mtype = 'warn'):
	############################################
	#	Print text w/ color
	#
	###########################################

	print(craft_msg(mtext, mtype))

def craft_msg(mtext, mtype = 'warn'):
	# https://misc.flogisoft.com/bash/tip_colors_and_formatting
	####################################################
	#	create text message with color
	#	bad: red
	#	warn: yellow
	#	good: light green
	#	This functions is using for Linux terminal only
	####################################################

	mtext = {
		'bad':  '\033[91m{}\033[00m'.format(mtext),
		'warn': '\033[93m{}\033[00m'.format(mtext),
		'good': '\033[92m{}\033[00m'.format(mtext),
		'norm': '\033[97m{}\033[00m'.format(mtext)
	}
	return (mtext[mtype])
	
def die(msg, error):
	printf("%s\n   %s" %(msg, error), "bad")
	sys.exit(1)

def print_table(headers, *args, **kwargs):
	################################################
	#	print beautiful table in terminal style
	#	author @routersploit project
	#	ALL input data must be string
	################################################

	extra_fill = kwargs.get("extra_fill", 2)
	header_separator = kwargs.get("header_separator", "-")
	if not all(map(lambda x: len(x) == len(headers), args)):
		printf("[x] PrintTable: Error headers", 'bad')
		return None

	def custom_len(x):
		try:
			return len(x)
		except TypeError:
			return 0

	##### CRAFTING HEADER ######
	fill = []

	# headers_line += label: Filling_header
	# headers_line = headers_line + "Lable 1 | Label 2"
	headers_line = '  |  '
	headers_separator_line = '  +'

	for idx, header in enumerate(headers):
		column = [custom_len(arg[idx]) for arg in args]
		column.append(len(header))
		current_line_fill = max(column) + extra_fill
		fill.append(current_line_fill)
		# label: Filling_header
		headers_line = "%s%s" %(
			"".join((headers_line, "{header:<{fill}}".format(header = header, fill = current_line_fill))),
			"|  "
			)

		headers_separator_line = "%s-%s" %(
			"-".join((
				headers_separator_line,
				'{:<{}}'.format(header_separator * current_line_fill, current_line_fill)
			)),
			"+"	
		)
		
	# End of crafting header

	# Print header
	print("%s\n%s\n%s" %(headers_separator_line, headers_line, headers_separator_line))

	# Print contents
	for arg in args:
		content_line = '  |  ' # print first character before contents
		for idx, element in enumerate(arg):
			content_line = "%s%s" %(
				"".join((
					content_line,
					'{:{}}'.format(element, fill[idx])
				)),
				"|  "	
			)
		print(content_line)
		
	# Print end line
	print(headers_separator_line)


def fixLen(text, lim):
	# https://stackoverflow.com/a/37422973
	ret, text = " %.*s" %(lim, text[:lim]), text[lim:]
	lim = 68 # MAX LIM FOR TERMINAL
	
	while text:
		
		if len(text) < lim:
			ret += " |\n  | %s" %(text) + " " * (lim + 1 - len(text))
			break
		ret, text = ret + " |\n  |  %.*s" %(71, text[:lim]), text[lim:]

	return ret

def report_banner(url, mode, proxy, thread, creds, daytime, runtime, regular):
	# if option != "--sqli" and "--single":
	def n_body(creds):
		ret = ""
		for match in creds:
			ret += "|  Username: %-58s |\n  |  Password: %-58s |" %(
				fixLen(match[0], 57), fixLen(match[1], 57)
			)
			ret += "\n  |%s|\n  " %("+" * 71)
		return ret
	
	def s_body(creds, mode):
		ret = ""
		name = "Payload" if mode == "--sqli" else "Password"
		for match in creds:
			payload = match[0] if match[0] else match[1]
			ret += "|  %-10s: %-56s |" %(
				name, 
				fixLen(payload, 48)
			)
			ret += "\n  |%s|\n  " %("+" * 71)
		return ret
	
	header = """
	  =====================================================================
	/       Finish: %-56s\\
	|       Name: %-57s |
	|-----------------------------------------------------------------------|
	|      Attack mode: %-6s |   Using Proxy: %-6s |   Threads: %-4s    |
	|-----------------------------------------------------------------------|
	|  Target: %-60s |
	|  URL: %-63s |
	|+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|
	""" %(
		"%s      %s" %(
			daytime.split("_")[1].replace(".", ":"),
			daytime.split("_")[0].replace(".", "/")
		),
		fixLen(daytime + ".txt", 55),
		mode.replace("--", ""),
		proxy,
		thread,
		fixLen(url.split("/")[2], 59),
		fixLen(url, 62),
	)
	
	footer = """\\  Runtime: %-60s/
	  =====================================================================\n""" %(runtime)
	
	body = n_body(creds) if regular else s_body(creds, mode)

	return header.replace("\t", "  ") + body + footer.replace("\t", "  ")

def start_banner(options):
	usr = options.options["-U"] if options.options["-U"] else options.options["-u"]

	banner = """
	  =====================================================================
	/%-71s\\
	|+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|
	|  Userlist: %-58s |
	|  Passlist: %-58s |
	|+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|
	|                                                                       |
	| %s |
	|                                                                       |
	|-----------------------------------------------------------------------|
	|    Extra mode: %-52s   |
	|-----------------------------------------------------------------------|
	|           Verbose: %-11s       |         Report: %-11s    |
	|***********************************************************************|
	|  %68s |
	+-----------------------------------------------------------------------+
	\\ %-69s /
	  =====================================================================
	""" %(
		" " * 23 + "HTTP LOGIN BRUTE FORCER",
		fixLen(usr, 57),
		fixLen(options.options["-p"], 57),
		fixLen( "Attack mode: %-6s |  Proxy: %-5s  |  Threads: %-3s |  Timeout: %-3s" %(
				options.attack_mode.replace("--", ""),
				options.run_options["--proxy"],
				options.threads,
				options.timeout,
			),
			68
		),
		"None" if len(options.extras) == 0 else fixLen(str(options.extras), 51),
		options.verbose,
		options.report,
		fixLen("%s target[s]: %-53s" %(
			len(options.target),
			options.options["-l"] if options.options["-l"] else (
				options.url.split("/")[2] if options.url.startswith(("http://", "https://")) else options.url.split("/")[0]
				)
			),
			67
		),
		" " * 11 + "Github: https://github.com/dmknght/BruteforceHTTP"
	)

	return banner.replace("\t", "  ")
	
if __name__ == "__main__":
	die("Oops! Wrong place", "Find other place")