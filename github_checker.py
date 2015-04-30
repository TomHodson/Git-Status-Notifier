from os import listdir, path
from subprocess import check_output
from time import gmtime, strftime

github_folder = "/Users/tom/Code/github"
output_format = \
"""
{repo_name} - {last_modified}
{underline}

{status}
"""

pressing_repos = []
number_of_orphan_files = 0

for f in listdir(github_folder):
	full_path = path.join(github_folder, f)
	if path.isdir(full_path):
		status = check_output(["git", "status"], cwd = full_path)
		time = strftime("%a, %d %b", gmtime(path.getmtime(full_path)))
		if "up-to-date" not in status:
			pressing_repos.append(output_format.format(repo_name = f,
			last_modified = time,
			status = status, 
			underline = '#' * (len(time) + len(f) + 2)))
	else: number_of_orphan_files += 1

if number_of_orphan_files:
	output.append("You have {n} orphaned files in your git directory that need homes.".format(n = number_of_orphan_files))

output =  "".join(pressing_repos)

if output:
	import smtplib
	server = smtplib.SMTP('smtp.gmail.com', 587)

	#Next, log in to the server
	server.ehlo()
	server.starttls()
	server.login("thomas.c.hodson@gmail.com", open("./secret").read())
	msg = "\r\n".join([
	  "From: thomas.c.hodson@gmail.com",
	  "To: thomas.c.hodson@gmail.com",
	  "Subject: Uncommited changes in {n} of your github repos".format(n = len(pressing_repos)),
	  "",
	  output
	  ])

	#Send the mail
	server.sendmail("thomas.c.hodson@gmail.com", "thomas.c.hodson@gmail.com", msg)
