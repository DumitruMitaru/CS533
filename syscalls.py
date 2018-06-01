import subprocess as sp
import os

# place the system call name, function call, extra code to run before the function call and how many times to run that code in 4 tuple in the list
# system call number are #defined to SYS_<name> in sys/syscall.h  http://unix.superglobalmegacorp.com/Net2/newsrc/sys/syscall.h.html,
# The code that you place in "syscall(SYS_fork)" or "open(test.txt)" will be injected into a .c file and compiled so it must be writte as c code. 
systemcalls = [
# ex
# ('name (can be whatever)', 'system call (must be in c)', 'extra code to run before system call (must be in c)', 'number of iterations'),

# Program Control
	('fork', 'syscall(SYS_fork);', '',1000), 
#	('wait' 'syscall(SYS_wait4, pid);', 'int pid = fork();', 1000),
	('brk', 'syscall(SYS_brk);', '', 1000),
# File Management
#	('open', 'syscall(SYS_open, "test.txt");', '', 1000),
	('close', 'syscall(SYS_close, fd);', 'int fd = open("test.txt", O_WRONLY);', 1000),
#	('read', 'syscall(SYS_read);', '', 1000),
#	('write', 'syscall(SYS_write);', '', 1000),
# Device Management
# Information Maintenence
	('getrusage', 'syscall(SYS_getrusage, RUSAGE_SELF, &usage', 'struct rusage usage;', 1000),
	('gettimeofday', 'syscall(SYS_gettimeofday, &t, NULL);', 'struct timeval t;', 1000),
# Communication
# ('sigaction', 'syscall(SYS_sigaction,...);, '', 1000) 
# ('sigreturn', 'syscall(SYS_sigreturn,...);, '', 1000) 
]

# delete old .c and executable files that will be generated by this program
def DeleteFiles():
	for name, c, e, r in systemcalls:
		os.remove(name + '.c')
		os.remove(name)

# create new exectuable files to run each system call
# and time it
def CreateNewFiles():
	for name, code, extra_code, runs in systemcalls:
		lines = open('template.c').readlines()
		new_filename = name + '.c'
		f1 = open(new_filename, 'w')	
		for line in lines:
			if 'XXX' in line:
				line = line.replace('XXX', code)
			if '// Extra Code' in line:
				line = line.replace('// Extra Code', extra_code)
			f1.write(line)
		f1.close()
		sp.call(['gcc', new_filename, '-o', new_filename[0:-2]])
	
	
# run each system call in the systemcalls array
def Run():
	for name, c, e, runs in systemcalls:
		output = ""
		for run in range(runs):
			output += sp.check_output(os.path.abspath(name))
		print name, average(output), 'usec'

def average(output):
	times = [int(i) for i in output.split(',')[0:-1]] 
	if -1 in times:
		return -1
	return sum(times) / float(len(times))
	
	
CreateNewFiles()
Run()
DeleteFiles()
