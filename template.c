#include <time.h>
#include <signal.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <sys/ioctl.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/vfs.h>
#include <ifaddrs.h>
#include <linux/random.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <sys/ipc.h>
#include <sys/msg.h>

struct message_buffer{
        long message_type;
        char message_text[10];
}message;

int main(int argc, char* argv[])
{
	struct timeval start;
	struct timeval end;
	long diff;
	long rc;
	int i;

	int sck_desc;
	struct sockaddr_in server;
	char *message_socket;
	char reply[500];

        // Pre-Exec Code
	gettimeofday(&start, NULL);
	for (i=0; i<YYY; ++i)
		rc = (long)XXX;
	gettimeofday(&end, NULL);
	// Post-Exec Code
	if(rc == -1)
		printf("-1");
	else
		diff = (end.tv_sec - start.tv_sec) * 1000000 + (end.tv_usec - start.tv_usec);
	printf("%li", diff);
	return 0;
}

// https://www.improgrammer.net/type-casting-c-language/
