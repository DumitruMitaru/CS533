#include <stdio.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <sys/ioctl.h>
#include <stdlib.h>
#include <fcntl.h>
#include <linux/random.h>

int main(int argc, char* argv[])
{
	struct timeval start;
	struct timeval end;
	long diff;
	int rc;
	// Extra Code
	gettimeofday(&start, NULL);
	rc = XXX;
	gettimeofday(&end, NULL);
	if(rc == -1)
		printf("-1,");
	else
		diff = (end.tv_sec - start.tv_sec) * 1000000 + (end.tv_usec - start.tv_usec);
	printf("%li,", diff);
}
