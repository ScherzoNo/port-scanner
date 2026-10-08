# Port Scanner
This project implements a simple TCP port scanner with multithreading. The user can either scan their localhost or a dedicated Nmap website.

# Description
The scanner places the ports specified by the user in a queue. Afterwards, a number of threads are created and started. Each thread tries to establish a TCP connection to each port in the queue, and when all of them finish their job, the program prints all of the open ports, if any.

Port range -> Queue -> Worker threads -> TCP connection attempts -> Open ports

## Usage
To run the code, execute the python file [`scanner.py`](./scanner.py).
