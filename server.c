// Server side C/C++ program to demonstrate Socket programming 
#include <unistd.h> 
#include <stdio.h> 
#include <sys/socket.h> 
#include <stdlib.h> 
#include <netinet/in.h> 
#include <string.h>
#define PORT 9000

enum { MAXC = 99999 };

// Convert english sentence to piglatin sentence
// From https://stackoverflow.com/questions/37176442/translating-a-sentence-to-pig-latin-in-c
void to_piglatin(char *english, char *piglatin)
{
    char *e = english, *p = piglatin;
    int c = 0, first = 1;

    /* for each char in english and len < MAXC - 2 */
    for (; *e && e - english + 2 < MAXC; e++) {
        if (('A' <= *e && *e < 'Z') || ('a' <= *e && *e < 'z')) {
            if (first == 1) {       /* if first char in word */
                c = *e, first = 0;  /* save, unset flag      */
                continue;           /* get next char         */
            }
            else
                *p++ = *e;          /* save char in piglatin */
        }
        else if (*e == ' ') {       /* if space, add c+'ay ' */
            *p++ = c, *p++ = 'a', *p++ = 'y', *p++ = *e;
            first = 1;              /* reset first flag  */
        }
    }   /*  add c+'ay ' for last word and print both */
    *p++ = c, *p++ = 'a', *p++ = 'y', *p++ = *e, *p = 0;
}


int main(int argc, char const *argv[]) { 
	int serversocket, clientsocket, valread; 
	struct sockaddr_in address; 
	int opt = 1; 
	int addrlen = sizeof(address); 
	char buffer[64] = {0}; 
    char output[MAXC] = "";
    int bind_outp, listen_outp, sent;
	
	// Creating socket file descriptor, same as python!
    serversocket = socket(AF_INET, SOCK_STREAM, 0);
	if (serversocket == 0) { 
		perror("socket failed"); 
		exit(EXIT_FAILURE); 
	} 
	
    // Some options
	address.sin_family = AF_INET; 
	address.sin_addr.s_addr = INADDR_ANY; 
	address.sin_port = htons( PORT ); 
    setsockopt(serversocket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    
    // Same commands as before, but checking errors in C because we're serious here
    bind_outp = bind(serversocket, (struct sockaddr *)&address, sizeof(address));
	if (bind_outp < 0) { 
		perror("bind failed"); 
		exit(EXIT_FAILURE); 
	}
    listen_outp = listen(serversocket, 3);
	if (listen_outp < 0) { 
		perror("listen"); 
		exit(EXIT_FAILURE); 
	}
    clientsocket = accept(serversocket, (struct sockaddr *)&address, (socklen_t*)&addrlen);
	if (clientsocket < 0) { 
		perror("accept"); 
		exit(EXIT_FAILURE); 
	} 
    
    // Same receiving loop as in the python version
    while(1) {
        memset(buffer, 0, 64);
        valread = recv(clientsocket, buffer, 64, 0);
        if (valread <= 0) break;
        
        printf("Received: %s\n", buffer); 
        printf("%d\n", valread);
        to_piglatin(buffer, output);
        
        // Same sending loop as in the python version
        for (int i = 0; i < strlen(output);) {
            sent = send(clientsocket , output , strlen(output) , 0); 
            printf("%d\n", sent);
            i += sent;
        }
        //printf("Hello message sent\n"); 
    }
    
    close(clientsocket);
    close(serversocket);

	return 0; 
} 
