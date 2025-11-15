/*------------------CHDIR.C
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <stdlib.h>
#include <linux/limits.h>

int main(int argc, char *argv[]) {
	char path[PATH_MAX]; 
	if (getcwd(path, PATH_MAX) == NULL)
		exit(1);
	printf("cwd %s\n",path);
	int err = chdir(argv[1]);
	if (err == -1)
		perror("execerr");
	if (getcwd(path, PATH_MAX) == NULL)
		exit(1);
	printf("cwd %s\n",path);
}*/
/*--------------------EXECERR.C
#include <stdio.h>
#include <unistd.h>
#include <errno.h>

int main(int argc, char *argv[]) {
	int err = execvp(argv[1], argv+1);
	printf("err = %d %d\n", err, errno);
	//if (errno == ENOENT) 
		//printf("non esiste\n");
	if (err == -1)
		perror("execerr");
}*/
/*-----------------------------LSTAT.C
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <stdlib.h>
#include <sys/stat.h>

int main(int argc, char *argv[]) {
	struct stat buf;
	int err = lstat(argv[1], &buf);
	if (err == -1) {
		perror("stat");
		exit(255);
	}
	printf("nlink %d\n", buf.st_nlink);
	printf("uid %d\n", buf.st_uid);
	printf("gid %d\n", buf.st_gid);
	printf("perm %o\n", buf.st_mode & 07777); //0xfff
	switch (buf.st_mode & S_IFMT) {
		case S_IFBLK:  printf("block device\n");            break;
		case S_IFCHR:  printf("character device\n");        break;
		case S_IFDIR:  printf("directory\n");               break;
		case S_IFIFO:  printf("FIFO/pipe\n");               break;
		case S_IFLNK:  printf("symlink\n");                 break;
		case S_IFREG:  printf("regular file\n");            break;
		case S_IFSOCK: printf("socket\n");                  break;
		default:       printf("unknown?\n");                break;
	}

}*/
/*---------------------------------STAT.C
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <stdlib.h>
#include <sys/stat.h>

int main(int argc, char *argv[]) {
	struct stat buf;
	int err = stat(argv[1], &buf);
	if (err == -1) {
		perror("stat");
		exit(255);
	}
	printf("nlink %d\n", buf.st_nlink);
	printf("uid %d\n", buf.st_uid);
	printf("gid %d\n", buf.st_gid);
	printf("perm %o\n", buf.st_mode & 07777); //0xfff
	switch (buf.st_mode & S_IFMT) {
		case S_IFBLK:  printf("block device\n");            break;
		case S_IFCHR:  printf("character device\n");        break;
		case S_IFDIR:  printf("directory\n");               break;
		case S_IFIFO:  printf("FIFO/pipe\n");               break;
		case S_IFLNK:  printf("symlink\n");                 break;
		case S_IFREG:  printf("regular file\n");            break;
		case S_IFSOCK: printf("socket\n");                  break;
		default:       printf("unknown?\n");                break;
	}

}*/