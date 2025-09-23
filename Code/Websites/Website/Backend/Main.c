// Dis is da backend thing using C for handling things \\.

// This is the includes/libraries/headers \\.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>
#include <ctype.h>

// This is the port you can change it to anything you want BUT you have to match it in script.js I'll put a variable you can change there \\.
#define PORT 5501

// These two functions fix the encodign from webservers so %40 turns into @ properly instead of showing "email%40email.com" \\.
char from_hex(char ch) {
    if (isdigit(ch)) return ch - '0';
    if (isupper(ch)) return ch - 'A' + 10;
    return ch - 'a' + 10;
}
void url_decode(char *str) {
    char *p = str;
    while (*str) {
        if (*str == '%' && isxdigit(str[1]) && isxdigit(str[2])) {
            *p++ = from_hex(str[1]) * 16 + from_hex(str[2]);
            str += 3;
        } else if (*str == '+') {
            *p++ = ' ';
            str++;
        } else { 
            *p++ = *str++;
        }
    }
    *p = '\0';
} 

// This handles the GET and POST requests from script.js \\.
void handle_request(int new_socket) {
    char buffer[2048] = {0};
    read(new_socket, buffer, sizeof(buffer));

    if (strncmp(buffer, "GET", 3) == 0) {

        char *response = // Response letting it know it went through \\.
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            "Access-Control-Allow-Origin: *\r\n"
            "Connection: close\r\n\r\n"
            "Sent"; // Message that prints in console.log in script.js \\.

        // Printing the lines of the file \\.
        FILE *fp = fopen("output.txt", "r");
        if (fp == NULL) {
            perror("Failed to open file");
            return;
        }
        char line[2048];
        int line_num = 1;
        while (fgets(line, sizeof(line), fp)) {
            printf("%d | %s", line_num, line);
            line_num++;
        }

        // Sending everything \\.
        write(new_socket, response, strlen(response));
        close(new_socket);

    } else if (strncmp(buffer, "POST", 4) == 0) {

        char *body = strstr(buffer, "\r\n\r\n");
        if (body) {
            body += 4;

            char *input_value = strstr(body, "data=");
            if (input_value) {
                input_value += 5;
                url_decode(input_value);

                // Appending to the output.txt file \\.
                FILE *fp = fopen("output.txt", "a");
                if (fp) {
                    fprintf(fp, "Email: %s\n", input_value);
                    fclose(fp);
                }
            }
        }
    }

    char *response = // Letting it know it went through ok \\.
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        "Access-Control-Allow-Origin: *\r\n"
        "Connection: close\r\n\r\n"
        "Saved successfully";
    
    // Sending the socket \\.
    write(new_socket, response, strlen(response));
    close(new_socket);
}

int main() {

    // Creating said socket \\.
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);

    server_fd = socket(AF_INET, SOCK_STREAM, 0);

    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 10);

    printf("C server running at http://localhost:%d\n", PORT); // Doesn't contribute anything you can remove but I keep it to let me know what port \\.

    // Constantly checks the socket \\.
    while (1) {
        new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen);
        if (new_socket >= 0) {
            handle_request(new_socket);
        }
    }

    return 0;
}
