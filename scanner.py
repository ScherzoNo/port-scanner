import socket
from queue import Queue
from threading import Thread


# check if the given port number by the user is valid
def valid_socket_input(arg: str) -> int:
    while True:
        try:
            nr = int(input(f"Insert the {arg} port number: \n"))

            # network port range numbers are 16-bit integers in the range 0-65535, but the port 0 is usually reserved
            if 1 <= nr <= 65535:
                return nr
            else:
                print("Input has to be a number between 1 and 65535")
        except ValueError:
            print("Invalid input type")


# check if the user selection is valid
def valid_host_selection() -> str:
    while True:

        # give the user a choice between selection 1 (localhost), or 2 (dedicated Nmap website)
        host_selection = input(
            "Type 1 to scan localhost, type 2 to scan a dedicated Nmap website: \n"
        )
        if host_selection == "1":
            return "127.0.0.1"
        elif host_selection == "2":
            
            # translate hostname to IP address with socket.gethostbyname, and catch any errors
            try:
                return socket.gethostbyname("scanme.nmap.org")
            except socket.gaierror:
                print("Could not resolve hostname")
        else:
            print("Invalid selection")
                     
def socket_cycle(host, q, open_ports) -> None:
    
    while True:
        port = q.get()
        
        # the worker's task is done when it sees None in the queue
        if port is None:
            q.task_done()
            break
        
        sock = socket.socket()

        # set a timeout for the socket so it doesn't take too long
        if host == "127.0.0.1":
            sock.settimeout(0.1)
        else:
            sock.settimeout(0.5)

        # connect_ex() returns 0 when the connection is successful
        if sock.connect_ex((host, port)) == 0:
            open_ports.append(port)
            
        # close the socket and mark the task as done in the queue by the thread
        sock.close() 
        q.task_done()
    


host = valid_host_selection()
first_port = valid_socket_input("first")
open_ports = []

while True:
    last_port = valid_socket_input("second")
    if first_port <= last_port:
        break
    print("Invalid range, try again")

# create the queue and fill it with the ports
q = Queue()
for i in range(first_port, last_port + 1):
    q.put(i)
   
num_threads = max(1, (last_port - first_port) // 10)

# fill the queue with a None for each worker, in order for the workers to understand when to exit
for _ in range(num_threads):
    q.put(None)
       
# create threads, give them a target, and start them
for i in range(num_threads):
    worker = Thread(target = socket_cycle, args = (host, q, open_ports))
    worker.start()
    
# wait for all the tasks to be done by the threads
q.join()

if not open_ports:
    print("No port is open")
else:
    open_ports.sort()
    print(f"Open ports: {open_ports}")