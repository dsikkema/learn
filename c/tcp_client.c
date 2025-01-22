#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>

int main() {
  int sock;
  struct sockaddr_in serv_addr;
  sock = socket(AF_INET, SOCK_STREAM, 0);
  if (sock < 0) {
    printf("Socket creation failed\n");
    return -1;
  }

  // config server address structure
  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(8080);
  
  // configure serv_addr to point at localhost
  if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) {
    printf("Invalid address\n");
    return -1;
  }
  
  if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
    printf("Conn failed\n");
    return -1;
  }

  printf("Connected to server\n");
  char buffer[1024] = {0};
  char* msg = "Hello, how are you?";
  while (1) {
    send(sock, msg, strlen(msg), 0);
    int bytes_read = read(sock, buffer, 1024);
    if (bytes_read <= 0) {
      printf("Connection was closed\n");
      break;
    }
    printf("%s", buffer);
  }
  close(sock);
  return 0;

}
