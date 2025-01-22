#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>


int main() {
  int server_fd; // socket file descriptor
  struct sockaddr_in address;

  // for help, try `man 2 socket`. 2 not 3, because this is a system call.
  // See how it's imported from sys/...?
  server_fd = socket(AF_INET, SOCK_STREAM, 0);
  if (server_fd < 0) {
    printf("Socket creation failed\n");
    return -1;
  }

  address.sin_family = AF_INET;
  address.sin_addr.s_addr = INADDR_ANY;
  address.sin_port = htons(8080);

  if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
    printf("Bind failed\n");
    return -1;
  }
  printf("Bind successful\n");
  
  if (listen(server_fd, 3) < 0) {
    printf("Listen failed\n");
    return -1;
  }
  printf("Server listening\n");

  char buffer[1024] = {0};
  int new_socket;
  int addrlen = sizeof(address);
  
  while(1) {
    new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen);
    while (1) {
      if (new_socket < 0) {
        printf("Accept failed\n");
        continue;
      }

      read(new_socket, buffer, 1024);
      printf("Client says: %s\n", buffer);

      char* response = "haha";
      send(new_socket, response, strlen(response) + 1, 0);
    }
    close(new_socket);
  }
}

