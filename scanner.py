import paramiko
import socket
import os

# Function to check SSH key length without authentication
def check_ssh_certificate_length(ip, port=22):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((ip, port))

        transport = paramiko.Transport(sock)
        transport.start_client()

        # Get the server's public key
        key = transport.get_remote_server_key()

        key_type = key.get_name()  # SSH-RSA, SSH-ED25519, etc.
        key_length = key.get_bits()  # Number of bits in the key

        print(f"IP: {ip} | Key Type: {key_type} | Key Length: {key_length} bits")

        # Close the connection
        transport.close()
        sock.close()

    except paramiko.SSHException as e:
        print(f"SSH error for {ip}: {str(e)}")
    except socket.error as e:
        print(f"Socket error while connecting to {ip}: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred for {ip}: {str(e)}")


# Function to read IPs from file and check cert length for each
def process_ips(file_name):
    if not os.path.exists(file_name):
        print(f"File {file_name} does not exist!")
        return
    
    with open(file_name, 'r') as file:
        ips = file.readlines()
    
    for ip in ips:
        ip = ip.strip()
        if ip:
            check_ssh_certificate_length(ip)

# Main
if __name__ == "__main__":
    # Path to file containing IP addresses (one IP per line)
    ip_file = "ip_addresses.txt"

    # Process each IP and check SSH certificate length without authentication
    process_ips(ip_file)
