import sys
import os
import subprocess
import socket
from time import localtime, strftime
import re
from optparse import OptionParser

path_to_nvcc_scanner = "data/nse7legacy/nvcc.exe"



def nvcc_scanner():
	if os.path.isfile(path_to_nvcc_scanner):
		env = os.environ.copy()
		env['WINEDEBUG'] = '-all'
		output = subprocess.Popen(["wine", path_to_officemalscanner,
			 "/U", "D:"], stdout = subprocess.PIPE, stderr = None, env=env).communicate()[0]
		if "Analysis finished" in output:
			output = output.split('\r\n')
			while "Analysis finished" not in output[0]:
				output = output[1:]
			result = output[3]
		else:
			result = "Not an executable file"
	else:
		result = 'ERROR - %s not found' % path_to_nvcc_scanner
	return ({'name': 'nvcc_scanner', 'result': result})

def filesize(data):
	return ({'name': 'filesize', 'result': str(len(data))})
	
def filename(filename):
	return({'name': 'filename', 'result': filename})

def main():
	parser = OptionParser()
	parser.add_option("-f", "--file", action="store", dest="filename",
	             type="string", help="scanned FILENAME")
	parser.add_option("-v", "--verbose", action="store_true", default=False,
					dest="verbose", help="verbose")

	(opts, args) = parser.parse_args()

	if opts.filename == None:
		parser.print_help()
		parser.error("You must supply a filename!")
	if not os.path.isfile(opts.filename):
		parser.error("%s does not exist" % opts.filename)
		
	data = open(opts.filename, 'rb').read()
	results = []
	results.append(filename(opts.filename))
	results.append(filesize(data))
	results.append(md5sum(data))
	results.append(officemalscanner(opts.filename))
#	results.append(fpscan(opts.filename))
#	results.append(cymruscan(data))
		
#	if opts.verbose:
#		print "[+] Using YARA signatures %s" % yara_conf_file
#		print "[+] Using ClamAV signatures %s" % clam_conf_file
#		print "\r\n"
	for result in results:
		if ("ERROR" in result['result']) and (opts.verbose == False):
			continue
		print "%20s\t%-s" % (result['name'],result['result'])
	print "\r\n"

if __name__ == '__main__':
	main()

