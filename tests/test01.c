#include <stdio.h> /* perror */
#include <unistd.h> /* sleep */
#include <stdlib.h> /* exit */
#include <sys/wait.h> /* waitpid */

static int worker(int depth)
{
	if (depth) {
		int pid;
	       
		pid = fork();
		if (pid < 0) {
			perror("fork");
			return 1;
		}
		if (pid == 0) {
			exit(worker(depth - 1));
		}

		if (!(depth % 2))
			waitpid(pid, NULL, 0);
	}

	if (depth % 2)
		return 0;

	while (1)
		sleep(1);

	return 0;
}

int main()
{
	exit(worker(20));
	return 0;
}
