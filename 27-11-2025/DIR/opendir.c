#include <stdio.h>
#include <dirent.h>

int main(){
	DIR * d=opendir(".");
	struct dirent * de;
	while((de=readdir(d))!=NULL){
		printf("%s\n",de->d_name);
	}
	closedir(d);


	return 0;
}
