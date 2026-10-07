import socket


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
            return "45.33.32.156"
        else:
            print("Invalid selection")


host = valid_host_selection()
first_port = valid_socket_input("first")

while True:
    last_port = valid_socket_input("second")
    if first_port <= last_port:
        break
    
    print("Invalid range, try again")

open_ports = []

# try to connect to every port in the indicated range
for port in range(first_port, last_port + 1):
    sock = socket.socket()

    # set a timeout for the socket so it doesn't take too long
    sock.settimeout(0.5)

    # connect_ex() returns 0 when the connection is successful
    if sock.connect_ex((host, port)) == 0:
        open_ports.append(port)
    sock.close()

print(open_ports)
