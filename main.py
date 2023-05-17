import os
import subprocess
import sys


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    print('Starting brute-fore-kit...')


print("""
 _                _          __                      _    _ _   
| |__  _ __ _   _| |_ ___   / _| ___  _ __ ___ ___  | | _(_) |_ 
| '_ \| '__| | | | __/ _ \ | |_ / _ \| '__/ __/ _ \ | |/ / | __|
| |_) | |  | |_| | ||  __/ |  _| (_) | | | (_|  __/ |   <| | |_ 
|_.__/|_|   \__,_|\__\___| |_|  \___/|_|  \___\___| |_|\_\_|\__|   
""")

print("""
+-+-+-+-+ +-+-+ +-+-+-+-+-+-+-+-+-+-+-+
|m|a|d|e| |b|y| |H|A|C|K|E|R|O|R|8|2|8|
+-+-+-+-+ +-+-+ +-+-+-+-+-+-+-+-+-+-+-+
""")

print("welcome Choose from the list:")
lst = [[1, 'ssh'], [2, 'ftp'], [3, 'smb'], [4, 'smtp']]
for i in lst:
    print(i[0], i[1])

while True:
    use = input("Choose an option (1, 2, 3, 4), or type 'exit' to quit: ")
    if use == 'exit':
        print("Bye!")
        break
    elif use == "1":
        print('SSH selected.')
        import ssh_brute_force
        ssh_brute_force.main()
        break
    elif use == "2":
        print("FTP selected.")
        import ftp_brute_force
        ftp_brute_force.main()
        break
    elif use == "3":
        print("SMB selected.")
        import smb_brute_force
        smb_brute_force.main()
        break
    elif use == "4":
        print("smtp selected.")
        import smtp_brute_force
        smtp_brute_force.main()
        break
    else:
        print("Invalid choice. Please choose a valid option.")
        continue
