#include <stdio.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <stdlib.h>
#include <fcntl.h>
#include <ifaddrs.h>

int main(int argc, char* argv[])
{
	struct timeval start;
	struct timeval end;
	long diff;
	int rc;
	struct timeval t;
	gettimeofday(&start, NULL);
	rc = syscall(SYS_gettimeofday, &t, NULL);;
	gettimeofday(&end, NULL);
	if(rc == -1)
		printf("-1,");
	else
		diff = (end.tv_sec - start.tv_sec) * 1000000 + (end.tv_usec - start.tv_usec);
	printf("%li,", diff);
}
