#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <time.h>
#include <pthread.h>
#include <wiringSerial.h>
#include <termios.h>
#include <stdlib.h>
#include <unistd.h>
#include <ctype.h>

#define READ_BUF_LEN 1024
#define SERIAL_DEVICE "/dev/ttyAMA0"  // RaspberryPi 2 Serial
#define SERIAL_BAUD 115200

int fd;
int commandReceived;

void processCommand();

void upperStr(char *s) {
    // Convert to upper case
    while (*s) {
        *s = (char)toupper((unsigned char)*s);
        s++;
    }
}

void rstBuffer(char *buffer) {
    // Empty receive buffer
    int i;
    for (i = 0; i < READ_BUF_LEN; i++)
        buffer[i] = '\0';
}

void *receiving(void *ptr) {
    // Thread for receiving SMS
    int gotData = 0;
    char buffer[READ_BUF_LEN];
    int pos = 0;
    double timeout = 0.5, elapsed;
    clock_t start = 0;

    rstBuffer(buffer);

    for (;;) {
        if (serialDataAvail(fd)) {
            if (start == 0)
                start = clock();

            while (serialDataAvail(fd)) {
                buffer[pos++] = (char)serialGetchar(fd);
                gotData = 1;
            }
        }

        if (gotData) {
            elapsed = ((double)clock() - (double)start) / CLOCKS_PER_SEC;
            if (elapsed > timeout) {
                printf("Received SMS: %s\n", buffer); 
                /* read from sensor to buffer */
                fwrite(buffer, sizeof(char), READ_BUF_LEN,  stdout); //#pypethon
                fflush(stdout);
                upperStr(buffer);
                // Reset buffer and variables to start listening again
                rstBuffer(buffer);
                pos = 0;
                gotData = 0;
                start = 0;
            }
        }
    }
    return NULL;
}

int setupSMS() {
    // Open serial device and setup modem
    fd = serialOpen(SERIAL_DEVICE, SERIAL_BAUD);

    if (fd < 0) {
        printf("Serial opening error\n");
        return 1;
    }

    pthread_t recThrd;
    int thr = pthread_create(&recThrd, NULL, receiving, NULL);
    if (thr != 0) {
        printf("Error during creating serialReceiver thread.");
        return 1;
    }

    pthread_detach(recThrd);

    return 0;
}

int main() {
    // Open and setup modem to receive SMS
    fd = -1;
    if (setupSMS() == 1) {
        close(fd);
        exit(1);
    }

    printf("Waiting SMS ...\n\n");

    for (;;) {
        // Process command sent by SMS to your modem
        processCommand();
        sleep(1);
    }

    printf("\n");
    return 0;
}