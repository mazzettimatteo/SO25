#include<stdio.h>
#include<unistd.h>
#include<errno.h>
#include<stdlib.h>
#include<sys/stat.h>

int main(int argc, int * argv[]){ 
	struct stat buf; 
	int err=lstat(argv[1],&buf);
	//lstat non esegue i link simbolici, quindi se gli passo un link questa volta mi dirà symlink, a differenza di stat()
	if(err==-1){ 
		perror("lstat"); 
		exit(89); 
	}
	printf("nlink %d\n",buf.st_nlink); 
	printf("uid %d\n",buf.st_uid); 
	printf("gid %d\n",buf.st_gid); 
	printf("perm %o\n",buf.st_mode & 07777); 
	
	switch(buf.st_mode & S_IFMT){ 
		case S_IFBLK: printf("block device\n");				break;
		case S_IFCHR: printf("charachter device\n");			break;
		case S_IFDIR: printf("directory\n");					break;
		case S_IFIFO: printf("FIFO/pipe\n");					break;
		case S_IFLNK: printf("symbolic link(soft)\n");		break;
		case S_IFREG: printf("regular file\n");				break;
		case S_IFSOCK: printf("socket\n");						break;
		default:		  printf("unknown \n");						break;
	}

}
