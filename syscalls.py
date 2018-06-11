import subprocess as sp
import os
import pdb

# place the system call name, function call, extra code to run before the function call and how many times to run that code in 4 tuple in the list
# system call number are #defined to SYS_<name> in sys/syscall.h  http://unix.superglobalmegacorp.com/Net2/newsrc/sys/syscall.h.html,
# The code that you place in "syscall(SYS_fork)" or "open(test.txt)" will be injected into a .c file and compiled so it must be writte as c code. 
systemcalls = [
# ex
# ('name (can be whatever)', 'system call (must be in c)', 'extra code to run before system call (must be in c)', 'number of iterations'),

# Process Control
	('fork', 'fork()', '', '', 1000), 
#	('getpid', 'getpid();', '',1000), 
	('kill', 'kill(pid, SIGKILL)', 'pid_t pid = fork(); if(pid == 0) while(1);', '', 1000), 
#	('wait', 'waitpid(pid, &status, WNOHANG);', 'pid_t pid = fork(); int status;', '', 1000),
	('brk', 'syscall(SYS_brk)', '', '', 1000),
	('mmap', 'mmap(NULL, st.st_size, PROT_READ, MAP_PRIVATE | MAP_POPULATE, fd, 0)', 'struct stat st; stat("test.txt", &st); int fd = open("test.txt", O_RDONLY, 0);', '', 1000),
	('munmap', ' 0; free(ptr)', 'int* ptr = malloc(10240000);', '', 1000),
# File Management
	('open', 'open("test.txt", O_WRONLY)', '', '', 1000),
	('close', 'close(fd)', 'int fd = open("test.txt", O_WRONLY);', '', 1000),
	('read', 'fscanf(fp,"%s", buff)', 'char buff[255]; FILE* fp = fopen("test.txt", "r");', 'fclose(fp);', 1000),
	('write', 'fprintf(fp, "datadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadata")', 'FILE* fp = fopen("test.txt", "w");', 'fclose(fp);', 1000),
# Device Management
	('ioctl_random', 'syscall(SYS_ioctl, fd, RNDZAPENTCNT, NULL)', 'int fd = open("/dev/random", O_RDONLY);', '', 1000),
	('ioctl_tty', 'syscall(SYS_ioctl, fd, TIOCGWINSZ, &winsz)', 'int fd = open("/dev/tty", O_RDONLY); struct winsize winsz;', '', 1000),
	('getitimer', 'syscall(SYS_getitimer, ITIMER_REAL, &curr_value)', 'struct itimerval curr_value;', '', 1000),
	('read_random', 'syscall(SYS_read, fd, &buf, 10)', 'int fd = open("/dev/urandom", O_RDONLY); char buf[10];', 'close(fd);', 1),
	('write_null', 'syscall(SYS_write, fd, "123456789", 10)', 'int fd = open("/dev/null", O_WRONLY);', 'close(fd);', 1000),
# Information Maintenence
	('getrusage', 'syscall(SYS_getrusage, RUSAGE_SELF, &usage)', 'struct rusage usage;', '', 1000),
	('stat', 'syscall(SYS_stat, "test.txt", &stat_buffer)', 'struct stat stat_buffer;', '', 1000),
  	('statfs', 'syscall(SYS_statfs, "test.txt", &statfs_buffer)', 'struct statfs statfs_buffer;', '', 1000),
  	('time', 'syscall(SYS_time, &time_struct)', 'time_t time_struct;', '', 1000), # would this take cre of stime?
  	('clock_gettime', 'syscall(SYS_clock_gettime, _POSIX_CPUTIME, &time_spec)', 'struct timespec time_spec;', '', 1000), 
# ('clock_getres', 'syscall(SYS_clock_getres, _POSIX_CPUTIME, &time_spec)', 'struct timespec time_spec;', 1000),
# ('clock_settime', 'syscall(SYS_clock_settime, _POSIX_CPUTIME, &time_spec)', 'struct timespec time_spec; time_spec.tv_sec = 64; time_spec.tv_nsec = 64;', 1000),
	('gettimeofday', 'gettimeofday(&time_val, NULL)', 'struct timeval time_val;', '', 1000),
	('getpid', 'getpid()', '', '', 1000),
#	('getppid', 'getppid()', '', 1000),
	('getuid', 'getuid()', '', '', 1000),
	('setuid', 'setuid(val)', 'uid_t val = getuid();', '', 1000), # Setting the process uid to the already existing uid should take as long as setting it elsewhere. Also, permissions may prohibit using any other value easily
#	('getgid', 'syscall(SYS_getppid)', '', 1000),
#	('stime', 'syscall(SYS_stime, &t);', 'time_t t;',1000),
	('getifaddrs', 'getifaddrs(&ifaddr)', 'struct ifaddrs *ifaddr, *ifa;', '', 1000),
	
# Communication
	('msgget', 'msgget(key, 0666|IPC_CREAT)', 'srand(time(0)); key_t key = ftok("/", rand());', 'msgctl((int)rc, IPC_RMID, NULL);', 1000),
        # msgget creates a message queue and returns identifier
        ('msgsnd', 'msgsnd(msgid, &message, sizeof(message), 0)', 'srand(time(0)); key_t key = ftok("/", rand()); int msgid = msgget(key, 0666 | IPC_CREAT); message.message_type = 1; strcpy(message.message_text, "data");', 'msgctl(msgid, IPC_RMID, NULL);', 1000),
        # msgsnd to send message
        ('msgrcv', 'msgrcv(msgid, &message, sizeof(message), 1, 0)', 'srand(time(0)); key_t key = ftok("/", rand()); int msgid = msgget(key, 0666 | IPC_CREAT); message.message_type = 1; strcpy(message.message_text, "write data"); msgsnd(msgid, &message, sizeof(message), 0);', 'msgctl(msgid, IPC_RMID, NULL);', 1000),
        # msgrcv to receive message
        ('msgctl', 'msgctl(msgid, IPC_RMID, NULL)', 'srand(time(0)); key_t key = ftok("/", rand()); int msgid = msgget(key, 0666 | IPC_CREAT);', '', 1000),
        # destroy the message queue with msgctl system call
	('create socket', 'socket(AF_INET , SOCK_STREAM , 0)', '', '', 1000),
        # create socket
        ('connect', 'connect(sck_desc , (struct sockaddr *)&server , sizeof(server))', 'sck_desc = socket(AF_INET , SOCK_STREAM , 0); server.sin_addr.s_addr = inet_addr("216.58.216.142"); server.sin_family = AF_INET; server.sin_port = htons(443);', 'close(sck_desc);', 1000),
        # connect to server
        ('send', 'send(sck_desc , message_socket , strlen(message_socket) , 0)', 'sck_desc = socket(AF_INET , SOCK_STREAM , 0); server.sin_addr.s_addr = inet_addr("216.58.216.142"); server.sin_family = AF_INET; server.sin_port = htons(443); connect(sck_desc , (struct sockaddr *)&server , sizeof(server)); message_socket = "GET / HTTP/1.1"; ', 'close(sck_desc);', 1000),
        # send 
        ('receive', 'recv(sck_desc, reply , 1000 , 0)', 'sck_desc = socket(AF_INET , SOCK_STREAM , 0); server.sin_addr.s_addr = inet_addr("216.58.216.142"); server.sin_family = AF_INET; server.sin_port = htons(443); connect(sck_desc , (struct sockaddr *)&server , sizeof(server)); message_socket = "GET / HTTP/1.1"; send(sck_desc , message_socket , strlen(message_socket) , 0);', 'close(sck_desc);', 50),
        # recieve
        ('close socket', 'close(sck_desc)', 'sck_desc = socket(AF_INET , SOCK_STREAM , 0); server.sin_addr.s_addr = inet_addr("216.58.216.142"); server.sin_family = AF_INET; server.sin_port = htons(443); connect(sck_desc , (struct sockaddr *)&server , sizeof(server));', '', 1000),
	# close socket
# ('sigaction', 'syscall(SYS_sigaction,...);, '', 1000) 
# ('sigreturn', 'syscall(SYS_sigreturn,...);, '', 1000) 
]

# delete old .c and executable files that will be generated by this program
def DeleteFiles():
	for name, c, pre, post, r in systemcalls:
		os.remove(name + '.c')
		os.remove(name)

# create new exectuable files to run each system call
# and time it
def CreateNewFiles():
	for name, code, pre_exec_code, post_exec_code, runs in systemcalls:
		lines = open('template.c').readlines()
		new_filename = name + '.c'
		f1 = open(new_filename, 'w')	
		for line in lines:
			if 'XXX' in line:
				line = line.replace('XXX', code)
			if '// Pre-Exec Code' in line:
				line = line.replace('// Pre-Exec Code', pre_exec_code)
			if '// Post-Exec Code' in line:
				line = line.replace('// Post-Exec Code', post_exec_code)
			f1.write(line)
		f1.close()
		sp.call(['gcc', new_filename, '-o', new_filename[0:-2]])
	
	
# run each system call in the systemcalls array
def Run():
	for name, c, pre, post, runs in systemcalls:
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


# References Used
# https://stackoverflow.com/questions/8798761/c-error-storage-size-of-a-isn-t-known
# https://stackoverflow.com/questions/8812959/how-to-read-linux-file-permission-programmatically-in-c-c
# http://man7.org/linux (various pages from here. Examples include http://man7.org/linux/man-pages/man2, and http://man7.org/linux/man-pages/man2/clock_getres.2.html)
# http://seclab.cs.sunysb.edu/sekar/papers/syscallclassif.htm
# https://linux.die.net/man/3/clock_settime
# https://linux.die.net/man/2/stime 
# http://man7.org/linux/man-pages/man3/fopen.3.html (and https://www.mathworks.com/matlabcentral/answers/276744-how-do-you-write-to-a-fopen-text-file-without-deleting-previous-text helped as well)
# https://www.odoo.com/forum/help-1/question/what-means-too-many-values-to-unpack-message-11679
# https://linux.die.net/man/2/msgctl
# Helped one of us figure out how to close a file descriptor: https://www.cs.bu.edu/teaching/c/file-io/intro/

# This helped one of us (who didn't write this portion of the script) understand the msgctl function: https://linux.die.net/man/2/msgctl

# These helped with socket connections: https://stackoverflow.com/questions/27665531/how-to-find-googles-ip-address and (https://serverfault.com/questions/357323/how-can-i-list-my-open-ports-on-debian and https://dns.google.com/ helped). 
# Google servers had been used in this test (the ip address of the server was 216.58.216.142). As such, credit and thanks to them must be given.
